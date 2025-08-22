"""
Analysis & Evaluation stage.

For Part 2, we implement lightweight analytics + a placeholder ML pipeline
that you can expand in Parts 3 and 4.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

def _basic_aggregations(df: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    if "calendar_year" in df.columns and "violations" in df.columns:
        yearly = df.groupby("calendar_year")["violations"].sum().reset_index()
        yearly.to_csv(out_dir / "agg_violations_yearly.csv", index=False)

    if "state_territory_tribe" in df.columns and "violations" in df.columns:
        state = df.groupby("state_territory_tribe")["violations"].sum().reset_index()
        state.to_csv(out_dir / "agg_violations_state.csv", index=False)

def run_analysis_pipeline(processed_path: Path, out_dir: Path) -> None:
    """
    Run descriptive analytics and (optionally) modeling on the processed dataset.
    Parameters
    ----------
    processed_path : Path
        Path to processed parquet (or CSV fallback).
    out_dir : Path
        Directory to write analysis outputs.
    """
    try:
        df = pd.read_parquet(processed_path)
    except Exception:
        df = pd.read_csv(processed_path.with_suffix(".csv"))

    # 1) Descriptive stats for sanity checks and evaluation
    _basic_aggregations(df, out_dir)

    # 2) Placeholder for modeling (e.g., predict high-violation systems)
    # TODO: feature engineering & ML (logistic regression / random forest).
    # Save evaluation metrics (precision/recall) to out_dir for Part 3/4 testing.
