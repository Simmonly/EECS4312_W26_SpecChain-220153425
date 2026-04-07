"""generates structured specs from personas"""
"""automated specification generation pipeline"""
import json
import os
from groq import Groq

# ── Config ─────────────────────────────────────────────────────────────────────
PERSONAS_PATH = 'personas/personas_auto.json'
SPEC_PATH     = 'spec/spec_auto.md'
MODEL         = 'meta-llama/llama-4-scout-17b-16e-instruct'

def generate_spec(personas, client):
    personas_text = json.dumps(personas, indent=2)

    prompt = f"""You are a software requirements engineer writing a formal specification for a meditation app called Medito.

Based on the following user personas, generate at least 10 structured software requirements.

For each requirement provide exactly this markdown format:

# Requirement ID: FR<number>
- **Description:** The system shall [specific measurable behavior]
- **Source Persona:** [persona id and name]
- **Traceability:** Derived from review group [group_id]
- **Acceptance Criteria:** Given [context] when [action] then [measurable outcome]

Rules:
- Write at least 10 requirements (FR1 to FR10 minimum)
- Every requirement must reference a persona id and group id
- Acceptance criteria must be specific and measurable, no vague terms like fast, easy, better
- Each requirement must be on a new line following the exact format above

Personas:
{personas_text}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=4000
    )

    return response.choices[0].message.content.strip(), prompt

def main():
    os.makedirs('spec', exist_ok=True)

    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not set!")
        return

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    print("Loading personas...")
    with open(PERSONAS_PATH, 'r') as f:
        personas_data = json.load(f)
    print(f"Loaded {len(personas_data['personas'])} personas")

    print("Generating specification with LLM...")
    spec_content, prompt = generate_spec(personas_data, client)

    # Add header
    header = "# Medito – Automated Software Specification\n## Pipeline: Automated | Source: personas/personas_auto.json\n\n---\n\n"
    with open(SPEC_PATH, 'w') as f:
        f.write(header + spec_content)
    print(f"Saved specification to {SPEC_PATH}")

if __name__ == '__main__':
    main()