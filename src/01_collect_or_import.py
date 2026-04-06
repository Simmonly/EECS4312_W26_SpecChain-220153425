"""imports or reads your raw dataset; if you scraped, include scraper here"""
from google_play_scraper import reviews, Sort
import json
from datetime import datetime

app_id = 'meditofoundation.medito'

result, _ = reviews(
    app_id,
    lang='en',
    country='us',
    sort=Sort.NEWEST,
    count=5000
)

def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

with open('data/reviews_raw.jsonl', 'w') as f:
    for review in result:
        f.write(json.dumps(review, default=serialize) + '\n')

print(f"Collected {len(result)} reviews")
