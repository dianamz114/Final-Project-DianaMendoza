# INST414 Final Project – Part 2 (EPA Final Data: Single CSV)

This repo implements a **Part 2** code package using your uploaded dataset: **EPA Final Data.csv**.

## Project Overview
- **Business Problem:** Identify high‑risk public water systems (PWS) for targeted oversight.
- **Dataset:** `EPA Final Data.csv` with columns like `PWS ID`, `Calendar Year`, `Violation Type`, `Violations`, etc.
- **Pipeline:** Extract (raw snapshot) → Transform (standardize/aggregate/label) → Model (logit & RF) → Evaluate → Visualize.

## Setup (VS Code)
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
# full pipeline
python main.py --stage all

# or stage-by-stage
python main.py --stage extract
python main.py --stage transform
python main.py --stage model
python main.py --stage evaluate
python main.py --stage vis
```

### Outputs
- `data/extracted/epa_final_data_raw.csv` (raw snapshot)
- `data/processed/merged_yearly.csv`, `facility_agg.csv`, `model_ready.csv`
- `data/outputs/models/*.joblib`, `data/outputs/metrics/model_metrics.json`
- `data/outputs/figures/*`

### Notes
- `high_risk_label` default: **≥3** violations in the last 3 years **or** total ≥3 (edit in `etl/transform.py`).
- Before submitting Part 2, run: `pip freeze > requirements.txt`
- Create Git branches: `dev`, `test`; keep Part 2 work on **dev**.
