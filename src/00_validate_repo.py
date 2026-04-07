"""checks required files/folders exist"""

import os

REQUIRED_FILES = [
    "data/reviews_raw.jsonl",
    "data/reviews_clean.jsonl",
    "data/dataset_metadata.json",
    "data/review_groups_manual.json",
    "data/review_groups_auto.json",
    "data/review_groups_hybrid.json",
    "personas/personas_manual.json",
    "personas/personas_auto.json",
    "personas/personas_hybrid.json",
    "spec/spec_manual.md",
    "spec/spec_auto.md",
    "spec/spec_hybrid.md",
    "tests/tests_manual.json",
    "tests/tests_auto.json",
    "tests/tests_hybrid.json",
    "metrics/metrics_manual.json",
    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",
    "metrics/metrics_summary.json",
    "prompts/prompt_auto.json",
    "reflection/reflection.md",
    "README.md",
    "src/00_validate_repo.py",
    "src/01_collect_or_import.py",
    "src/02_clean.py",
    "src/05_personas_auto.py",
    "src/06_spec_generate.py",
    "src/07_tests_generate.py",
    "src/08_metrics.py",
    "src/run_all.py",
]

def main():
    print("\nChecking repository structure...")
    print("="*50)

    all_found = True
    for filepath in REQUIRED_FILES:
        if os.path.exists(filepath):
            print(f"  ✓  {filepath} found")
        else:
            print(f"  ✗  {filepath} MISSING")
            all_found = False

    print("="*50)
    if all_found:
        print("Repository validation complete — all files present!")
    else:
        print("Repository validation FAILED — some files are missing.")

if __name__ == '__main__':
    main()