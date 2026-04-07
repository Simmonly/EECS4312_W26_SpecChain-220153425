"""generates tests from specs"""
"""automated test generation pipeline"""
import json
import os
import re
from groq import Groq

# ── Config ─────────────────────────────────────────────────────────────────────
SPEC_PATH   = 'spec/spec_auto.md'
TESTS_PATH  = 'tests/tests_auto.json'
MODEL       = 'meta-llama/llama-4-scout-17b-16e-instruct'

def extract_requirement_ids(spec_content):
    """Extract all FR IDs from the spec file."""
    return re.findall(r'FR\d+', spec_content)

def generate_tests(spec_content, client):
    prompt = f"""You are a software QA engineer writing validation tests for a meditation app called Medito.

Based on the following software specification, generate at least 2 test scenarios per requirement.

Respond ONLY with a valid JSON object in this exact format, no preamble or explanation:
{{
  "tests": [
    {{
      "test_id": "T_auto_1a",
      "requirement_id": "FR1",
      "scenario": "short scenario title",
      "steps": [
        "step 1",
        "step 2",
        "step 3"
      ],
      "expected_result": "specific measurable expected outcome"
    }}
  ]
}}

Rules:
- Generate at least 2 test scenarios per requirement
- test_id format must be T_auto_<number><letter> (e.g. T_auto_1a, T_auto_1b)
- Every test must reference a valid requirement_id from the spec
- Steps must be clear and specific
- Expected result must be measurable, not vague

Specification:
{spec_content}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw), prompt

def main():
    os.makedirs('tests', exist_ok=True)

    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not set!")
        return

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    print("Loading specification...")
    with open(SPEC_PATH, 'r') as f:
        spec_content = f.read()

    req_ids = extract_requirement_ids(spec_content)
    unique_reqs = list(dict.fromkeys(req_ids))
    print(f"Found {len(unique_reqs)} requirements: {unique_reqs}")

    print("Generating tests with LLM...")
    tests_data, prompt = generate_tests(spec_content, client)

    with open(TESTS_PATH, 'w') as f:
        json.dump(tests_data, f, indent=2)
    print(f"Saved {len(tests_data['tests'])} tests to {TESTS_PATH}")

if __name__ == '__main__':
    main()