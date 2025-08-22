# Final Project – Part 2 – Diana Mendoza

**GitHub URL:** https://github.com/dianamz114/Final-Project-DianaMendoza

## Change Log
| Change | Reason |
|---|---|
| Set up repo scaffold with ETL/analysis/vis modules | Align with pipeline-first design and grading rubric |
| Added data dictionary and reference tables | Improves clarity, supports joins and viz labels |
| Implemented processing of calendar year + violations | Standardize types for analysis |
| Generated initial EDA outputs (CSV) | Baseline checks; artifacts for Parts 3–4 tests |
| Drafted visualization functions | Exploratory figures for trends and state comparisons |

---

## 1. Project Setup
**Repo & branches:** `main`, `dev`, `test`. Code for Part 2 lives on `dev`.<br>
**Environment:** Python venv with `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `pyarrow`.<br>
**Entry point:** `main.py` orchestrates `extract → transform → load → analysis → visualize`.<br>

## 2. ETL Pipeline
**Extract:** For Part 2, we load a local CSV (`EPA_Final_Data.csv`) placed in `data/extracted/`. In Part 3/4, this can be swapped for an API or ECHO bulk download.<br>
**Transform:** Normalize column names, parse `Calendar Year` → int, coerce `Violations` to numeric, de-duplicate rows, and create `pws_year_id`. Simple EDA artifacts (missingness, dtypes, totals by year/state) are written to `data/outputs/`.<br>
**Load:** Persist processed data to `data/processed/epa_processed.parquet` (with CSV fallback).

## 3. Analysis and Evaluation
**Descriptive analytics:** Aggregations of total violations by **year** and by **state/territory/tribe**.<br>
**Modeling plan (Part 3/4):** Predict high-violation PWS/year observations using features like system size, source water, population served, and prior violations. Start with logistic regression; compare with tree-based models. Evaluate with precision/recall/AUROC and stratify by state.<br>

## 4. Visualization and Presentation Development
**Figures (Part 2):** Trend of violations over time; Top states by total violations.<br>
**Planned (Part 3/4):** Add small multiples by source water; per-capita normalization by population served; interactive dashboard if time allows.

## 5. Code, Data, and Project Management
**Documentation:** All functions include docstrings; `README.md` has overview, setup, run instructions, and structure.<br>
**Data dictionaries:** `data/reference-tables/data_dictionary_epa_final_data.csv` auto-generated; `data/reference-tables/us_states.csv` supports label lookups.<br>

## 6. Challenges and Solutions
- **Column heterogeneity:** Calendar years stored as strings like `CY 2023`. *Solution:* regex parse to extract the 4-digit year.
- **Type coercion & missingness:** Violations sometimes non-numeric. *Solution:* `to_numeric(..., errors="coerce")` + explicit checks in EDA.
- **Scoping ML for Part 2:** Full modeling deferred. *Solution:* Implemented descriptive pipeline and a clear modeling roadmap for Parts 3 and 4.
