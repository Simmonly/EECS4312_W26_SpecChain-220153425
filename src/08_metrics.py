"""metrics computation for all three pipelines"""
import json
import os
import re

# ── Config ─────────────────────────────────────────────────────────────────────
PIPELINES = {
    'manual': {
        'reviews':    'data/reviews_clean.jsonl',
        'groups':     'data/review_groups_manual.json',
        'personas':   'personas/personas_manual.json',
        'spec':       'spec/spec_manual.md',
        'tests':      'tests/tests_manual.json',
        'output':     'metrics/metrics_manual.json'
    },
    'auto': {
        'reviews':    'data/reviews_clean.jsonl',
        'groups':     'data/review_groups_auto.json',
        'personas':   'personas/personas_auto.json',
        'spec':       'spec/spec_auto.md',
        'tests':      'tests/tests_auto.json',
        'output':     'metrics/metrics_auto.json'
    },
    'hybrid': {
        'reviews':    'data/reviews_clean.jsonl',
        'groups':     'data/review_groups_hybrid.json',
        'personas':   'personas/personas_hybrid.json',
        'spec':       'spec/spec_hybrid.md',
        'tests':      'tests/tests_hybrid.json',
        'output':     'metrics/metrics_hybrid.json'
    }
}

AMBIGUOUS_TERMS = [
    'fast', 'quickly', 'easy', 'easily', 'better', 'good', 'nice',
    'user-friendly', 'simple', 'smooth', 'intuitive', 'reasonable',
    'appropriate', 'adequate', 'sufficient', 'improved', 'efficient'
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def count_reviews(path):
    count = 0
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                count += 1
    return count

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def extract_requirement_ids_from_spec(spec_path):
    with open(spec_path, 'r') as f:
        content = f.read()
    return list(dict.fromkeys(re.findall(r'FR\d+', content)))

def extract_persona_ids_from_spec(spec_path):
    with open(spec_path, 'r') as f:
        content = f.read()
    return re.findall(r'P\d+', content)

def count_ambiguous_requirements(spec_path):
    with open(spec_path, 'r') as f:
        content = f.read()
    req_blocks = re.split(r'# Requirement ID:', content)[1:]
    ambiguous = 0
    for block in req_blocks:
        block_lower = block.lower()
        if any(term in block_lower for term in AMBIGUOUS_TERMS):
            ambiguous += 1
    return ambiguous, len(req_blocks)

def compute_metrics(pipeline_name, paths):
    print(f"\nComputing metrics for: {pipeline_name}")
    metrics = {"pipeline": pipeline_name}

    # Dataset size
    metrics['dataset_size'] = count_reviews(paths['reviews'])

    # Persona count
    personas_data = load_json(paths['personas'])
    personas = personas_data.get('personas', [])
    metrics['persona_count'] = len(personas)

    # Requirements count
    req_ids = extract_requirement_ids_from_spec(paths['spec'])
    metrics['requirements_count'] = len(req_ids)

    # Tests count
    tests_data = load_json(paths['tests'])
    tests = tests_data.get('tests', [])
    metrics['tests_count'] = len(tests)

    # Traceability links
    # persona->group links + requirement->persona links
    groups_data = load_json(paths['groups'])
    group_links = len(groups_data.get('groups', []))
    persona_links = len(personas)
    metrics['traceability_links'] = group_links + persona_links

    # Review coverage ratio
    all_evidence_ids = set()
    for p in personas:
        for rid in p.get('evidence_reviews', []):
            all_evidence_ids.add(rid)
    metrics['review_coverage'] = round(len(all_evidence_ids) / metrics['dataset_size'], 4)

    # Traceability ratio
    persona_ids_in_spec = extract_persona_ids_from_spec(paths['spec'])
    req_ids_with_persona = set()
    with open(paths['spec'], 'r') as f:
        content = f.read()
    req_blocks = re.split(r'# Requirement ID:', content)[1:]
    for block in req_blocks:
        fr_match = re.search(r'FR\d+', block)
        p_match  = re.search(r'P\d+', block)
        if fr_match and p_match:
            req_ids_with_persona.add(fr_match.group())
    metrics['traceability_ratio'] = round(
        len(req_ids_with_persona) / len(req_ids) if req_ids else 0, 4
    )

    # Testability rate
    tested_reqs = set(t.get('requirement_id') for t in tests)
    metrics['testability_rate'] = round(
        len(tested_reqs.intersection(set(req_ids))) / len(req_ids) if req_ids else 0, 4
    )

    # Ambiguity ratio
    ambiguous_count, total_reqs = count_ambiguous_requirements(paths['spec'])
    metrics['ambiguity_ratio'] = round(
        ambiguous_count / total_reqs if total_reqs > 0 else 0, 4
    )

    return metrics

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    os.makedirs('metrics', exist_ok=True)
    all_metrics = {}

    for pipeline_name, paths in PIPELINES.items():
        # Skip if files don't exist yet (e.g. hybrid not built yet)
        if not os.path.exists(paths['personas']):
            print(f"Skipping {pipeline_name} — files not found yet")
            continue

        metrics = compute_metrics(pipeline_name, paths)
        all_metrics[pipeline_name] = metrics

        with open(paths['output'], 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"Saved to {paths['output']}")

    # Save summary
    summary = {
        "summary": all_metrics,
        "comparison_notes": {
            "dataset_size": "Same across all pipelines — 4115 cleaned reviews",
            "persona_count": "Number of personas generated per pipeline",
            "requirements_count": "Number of FR requirements in each spec",
            "tests_count": "Total test scenarios generated",
            "review_coverage": "Ratio of reviews referenced in persona evidence",
            "traceability_ratio": "Proportion of requirements traceable to a persona",
            "testability_rate": "Proportion of requirements with at least one test",
            "ambiguity_ratio": "Proportion of requirements containing vague language"
        }
    }
    with open('metrics/metrics_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("\nSaved metrics/metrics_summary.json")

if __name__ == '__main__':
    main()