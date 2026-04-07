"""automated persona generation pipeline"""
import json
import os
import random
from groq import Groq

# ── Config ─────────────────────────────────────────────────────────────────────
CLEAN_PATH     = 'data/reviews_clean.jsonl'
GROUPS_PATH    = 'data/review_groups_auto.json'
PERSONAS_PATH  = 'personas/personas_auto.json'
PROMPTS_PATH   = 'prompts/prompt_auto.json'
MODEL          = 'meta-llama/llama-4-scout-17b-16e-instruct'

# ── Load reviews ───────────────────────────────────────────────────────────────
def load_reviews(path, sample_size=200):
    reviews = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                reviews.append(json.loads(line))
    random.seed(42)
    return random.sample(reviews, min(sample_size, len(reviews)))

# ── Step 4.1: Group reviews ────────────────────────────────────────────────────
def group_reviews(reviews, client):
    review_text = "\n".join([
        f"ID: {r['reviewId']} | Score: {r['score']} | Review: {r['cleaned_content']}"
        for r in reviews
    ])

    prompt = f"""You are a software requirements engineer analyzing user reviews for a meditation app called Medito.

Below are user reviews. Group them into exactly 5 thematic groups based on common user needs, complaints, or experiences.

For each group provide:
- group_id (G1 to G5)
- theme (short descriptive label)
- review_ids (list of IDs belonging to this group, at least 10 per group)
- example_reviews (2-3 short representative quotes)

Respond ONLY with a valid JSON object in this exact format, no preamble or explanation:
{{
  "groups": [
    {{
      "group_id": "G1",
      "theme": "...",
      "review_ids": ["id1", "id2", ...],
      "example_reviews": ["quote1", "quote2"]
    }}
  ]
}}

Reviews:
{review_text}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw), prompt

# ── Step 4.2: Generate personas ────────────────────────────────────────────────
def generate_personas(groups, client):
    groups_text = json.dumps(groups, indent=2)

    prompt = f"""You are a UX researcher creating user personas for a meditation app called Medito.

Based on the following review groups, create one detailed persona per group.

For each persona provide:
- id (P1 to P5)
- name (a descriptive persona name)
- description (2-3 sentence summary)
- derived_from_group (group_id)
- goals (list of 3 goals)
- pain_points (list of 3 pain points)
- context (list of 2-3 contextual situations)
- constraints (list of 2-3 constraints)
- evidence_reviews (list of 3-5 review IDs from the group)

Respond ONLY with a valid JSON object, no preamble or explanation:
{{
  "personas": [...]
}}

Review Groups:
{groups_text}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw), prompt

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    os.makedirs('data', exist_ok=True)
    os.makedirs('personas', exist_ok=True)
    os.makedirs('prompts', exist_ok=True)

    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not set!")
        return

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    print("Loading reviews...")
    reviews = load_reviews(CLEAN_PATH, sample_size=200)
    print(f"Sampled {len(reviews)} reviews for grouping")

    print("Grouping reviews with LLM...")
    groups_data, group_prompt = group_reviews(reviews, client)

    with open(GROUPS_PATH, 'w') as f:
        json.dump(groups_data, f, indent=2)
    print(f"Saved {len(groups_data['groups'])} groups to {GROUPS_PATH}")

    print("Generating personas with LLM...")
    personas_data, persona_prompt = generate_personas(groups_data, client)

    with open(PERSONAS_PATH, 'w') as f:
        json.dump(personas_data, f, indent=2)
    print(f"Saved {len(personas_data['personas'])} personas to {PERSONAS_PATH}")

    prompts = {
        "grouping_prompt": group_prompt,
        "persona_prompt": persona_prompt,
        "model": MODEL
    }
    with open(PROMPTS_PATH, 'w') as f:
        json.dump(prompts, f, indent=2)
    print(f"Saved prompts to {PROMPTS_PATH}")

if __name__ == '__main__':
    main()