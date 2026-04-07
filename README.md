# EECS4312_W26_SpecChain

## Application: Medito

## Data Collection
- Collection method: google-play-scraper Python library 
- App ID: meditofoundation.medito
- Platform: Google Play Store

## Dataset
- reviews_raw.jsonl: contains the raw data collected from the website
- reviews_clean.jsonl: contains the cleaned data
- The original dataset contains 5,000 reviews
- The cleaned dataset contains 4,115 reviews
- 885 reviews were removed: 624 for being too short, 261 for having duplicate content

## Repository Structure
- data/: data sets and review groups
- personas/ persona files and pipelines
- spec/: specificaiton files for the pipelines
- tests/: validaiton tests for the pipelines
- metrics/: metric files and summary comparison
- prompts/: contains the LLM prompts used in the automated pipelines
- src/: all executable python files
- reflection/: the final reflection 

## How to Run
1. python src/00_validate_repo.py
2. python src/01_collect_or_import.py
3. python src/02_clean.py
4. python src/run_all.py
5. Open metrics/metrics_summary.json for comparison results

## Metrics Summary

| Metric | Manual | Auto | Hybrid |
|---|---|---|---|
| Dataset Size | 4115 | 4115 | 4115 |
| Persona Count | 5 | 5 | 5 |
| Requirements Count | 12 | 10 | 12 |
| Tests Count | 24 | 20 | 24 |
| Traceability Ratio | 1.0 | 1.0 | 1.0 |
| Testability Rate | 1.0 | 1.0 | 1.0 |
| Ambiguity Ratio | 0.0 | 0.3 | 0.0 |

## Notes
- The automated pipeline samples 200 reviews for LLM grouping to stay
  within API token limits. The full 4,115 review dataset is used for
  all metric computations.
- The Groq API with meta-llama/llama-4-scout-17b-16e-instruct was used
  for all LLM-based generation steps.
- Manual and hybrid artifacts were produced with my judgment and
  not by run_all.py.
- Set up your Groq API key before running with: export GROQ_API_KEY=your_key_here
