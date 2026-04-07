"""runs the full pipeline end-to-end"""

import subprocess
import sys
import os

SCRIPTS = [
    ("01_collect_or_import.py", "Collecting raw reviews from Google Play..."),
    ("02_clean.py",             "Cleaning and preprocessing reviews..."),
    ("05_personas_auto.py",     "Grouping reviews and generating personas via LLM..."),
    ("06_spec_generate.py",     "Generating specification from personas via LLM..."),
    ("07_tests_generate.py",    "Generating tests from specification via LLM..."),
    ("08_metrics.py",           "Computing metrics for all pipelines..."),
]

def run_script(script_name, description):
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"Running: src/{script_name}")
    print('='*60)

    result = subprocess.run(
        [sys.executable, f"src/{script_name}"],
        capture_output=False
    )

    if result.returncode != 0:
        print(f"\nERROR: {script_name} failed with exit code {result.returncode}")
        print("Stopping pipeline.")
        sys.exit(1)

    print(f"✓ {script_name} completed successfully")

def main():
    print("\nSpecChain Automated Pipeline")
    print("="*60)
    print("Starting full automated pipeline run...")

    if not os.environ.get("GROQ_API_KEY"):
        print("\nERROR: GROQ_API_KEY environment variable is not set.")
        print("Please run: export GROQ_API_KEY=your_key_here")
        sys.exit(1)

    for script_name, description in SCRIPTS:
        run_script(script_name, description)

    print(f"\n{'='*60}")
    print("Pipeline complete! Files produced:")
    print("  data/reviews_raw.jsonl")
    print("  data/reviews_clean.jsonl")
    print("  data/dataset_metadata.json")
    print("  data/review_groups_auto.json")
    print("  personas/personas_auto.json")
    print("  prompts/prompt_auto.json")
    print("  spec/spec_auto.md")
    print("  tests/tests_auto.json")
    print("  metrics/metrics_auto.json")
    print("  metrics/metrics_summary.json")
    print("="*60)

if __name__ == '__main__':
    main()