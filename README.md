# EPA Drinking Water Violations — Final Project (Part 2)

This repository contains the **Part 2** technical development for a data science pipeline focused on U.S. Safe Drinking Water Act (SDWA) **public water system (PWS)** violations.

## Project Overview
- **Business problem**: Help agencies and communities understand **where and when violations occur**, identify factors correlated with high-violation systems, and provide **evidence for prioritizing inspections and interventions**.
- **Primary dataset**: EPA ECHO SDWA extract (included here as `data/extracted/EPA_Final_Data.csv`).
- **Key stages**: ETL → Analysis → Visualization.
- **Expected outputs**: Processed/tidy data, descriptive aggregates by year/state, and charts (trend over time; top states).

## Setup Instructions
```bash
# 1) Clone your repo (replace with your URL)
git clone <YOUR_REPO_URL>.git
cd inst414-final-project-diana-mendoza

# 2) Create & activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt
```

## Running the Project
```bash
# Run full pipeline
python main.py --run all

# Or run a specific stage
python main.py --run extract
python main.py --run transform
python main.py --run analysis
python main.py --run visualize
```

## Code Package Structure
```
inst414-final-project-diana-mendoza/
├── data/
│   ├── extracted/            # Raw/source data (input-only)
│   ├── processed/            # Cleaned, analysis-ready data
│   ├── outputs/              # Analysis outputs (aggregates, metrics)
│   └── reference-tables/     # Data dictionaries & static reference lookups
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── analysis/
│   └── model.py
├── vis/
│   └── visualizations.py
├── scripts/
│   └── make_data_dictionary.py
├── main.py
├── README.md
└── requirements.txt
```

## Notes
- For submission, regenerate `requirements.txt` after your final environment setup:
  ```bash
  pip freeze > requirements.txt
  ```
- Add your instructors as collaborators on GitHub as required by the assignment.
