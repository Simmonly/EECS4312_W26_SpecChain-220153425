"""cleans raw data & make clean dataset"""
import json
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

RAW_PATH   = 'data/reviews_raw.jsonl'
CLEAN_PATH = 'data/reviews_clean.jsonl'
META_PATH  = 'data/dataset_metadata.json'

stop_words  = set(stopwords.words('english'))
lemmatizer  = WordNetLemmatizer()

NUMBER_MAP = {
    '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
    '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
}

def convert_numbers(text):
    """Replace standalone digits with their word equivalents."""
    return re.sub(r'\b(\d+)\b', lambda m: ' '.join(NUMBER_MAP.get(c, c) for c in m.group()), text)

def clean_text(text):
    # 1. Remove emojis and non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    # 2. Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # 3. Remove special characters and punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 4. Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # 5. Convert to lowercase
    text = text.lower()
    # 6. Convert numbers to words
    text = convert_numbers(text)
    # 7. Remove stop words
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words]
    # 8. Lemmatize
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return ' '.join(tokens)

def main():
    raw_reviews = []
    with open(RAW_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                raw_reviews.append(json.loads(line))

    print(f"Raw reviews loaded: {len(raw_reviews)}")

    seen_ids   = set()
    seen_texts = set()
    cleaned    = []
    skipped    = {'duplicate_id': 0, 'duplicate_text': 0, 'empty': 0, 'too_short': 0}

    for review in raw_reviews:
        review_id = review.get('reviewId', '')
        raw_text  = review.get('content', '') or ''

        # Remove duplicates by ID
        if review_id in seen_ids:
            skipped['duplicate_id'] += 1
            continue
        seen_ids.add(review_id)

        # Remove empty entries
        if not raw_text.strip():
            skipped['empty'] += 1
            continue

        # Remove extremely short reviews (fewer than 3 words)
        if len(raw_text.split()) < 3:
            skipped['too_short'] += 1
            continue

        cleaned_text = clean_text(raw_text)

        # Remove duplicate content after cleaning
        if cleaned_text in seen_texts:
            skipped['duplicate_text'] += 1
            continue
        seen_texts.add(cleaned_text)

        cleaned.append({
            'reviewId':       review_id,
            'cleaned_content': cleaned_text,
            'original_content': raw_text,
            'score':          review.get('score'),
            'at':             review.get('at'),
            'userName':       review.get('userName', '')
        })

    with open(CLEAN_PATH, 'w', encoding='utf-8') as f:
        for r in cleaned:
            f.write(json.dumps(r) + '\n')

    print(f"Cleaned reviews saved: {len(cleaned)}")
    print(f"Skipped — {skipped}")

    metadata = {
        'app_name':          'Medito',
        'app_id':            'meditofoundation.medito',
        'collection_method': 'google-play-scraper Python library (Sort.NEWEST)',
        'raw_review_count':  len(raw_reviews),
        'clean_review_count': len(cleaned),
        'skipped':           skipped,
        'cleaning_steps': [
            'Removed non-ASCII characters and emojis',
            'Removed URLs',
            'Removed punctuation and special characters',
            'Removed extra whitespace',
            'Converted to lowercase',
            'Converted digits to words',
            'Removed English stop words (NLTK)',
            'Lemmatized tokens (NLTK WordNetLemmatizer)',
            'Removed duplicate review IDs',
            'Removed empty reviews',
            'Removed reviews with fewer than 3 words',
            'Removed duplicate cleaned content'
        ]
    }

    with open(META_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved to {META_PATH}")

if __name__ == '__main__':
    main()