"""
ETL - Transform stage.

Cleans and wrangles the raw data into an analysis-ready table.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np

def _clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
                  .str.lower()
                  .str.replace(r"[^0-9a-zA-Z]+", "_", regex=True)
                  .str.strip("_")
    )
    return df

def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Calendar Year as int (e.g., "CY 2023" -> 2023)
    if "calendar_year" in df.columns:
        df["calendar_year"] = (
            df["calendar_year"]
            .astype(str)
            .str.extract(r"(\d{4})", expand=False)
            .astype("Int64")
        )
    # Violations as numeric
    if "violations" in df.columns:
        df["violations"] = pd.to_numeric(df["violations"], errors="coerce")
    return df

def _add_ids(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Create robust unique ID for row-level analysis
    if {"pws_id", "calendar_year"}.issubset(df.columns):
        df["pws_year_id"] = df["pws_id"].astype(str) + "-" + df["calendar_year"].astype(str)
    return df

def _dedupe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates()
    return df

def _eda_artifacts(df: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    profile = {
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": df.columns.tolist(),
        "missing_by_col": df.isna().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }
    (out_dir / "eda_summary.json").write_text(pd.Series(profile).to_json(indent=2))

    # Simple aggregations useful for testing later
    if "state_territory_tribe" in df.columns and "violations" in df.columns:
        by_state = df.groupby("state_territory_tribe")["violations"].sum().sort_values(ascending=False)
        by_state.to_csv(out_dir / "violations_by_state.csv")

    if "calendar_year" in df.columns and "violations" in df.columns:
        by_year = df.groupby("calendar_year")["violations"].sum().sort_values(ascending=False)
        by_year.to_csv(out_dir / "violations_by_year.csv")

def transform_epa_data(raw_csv_path: Path, processed_out_path: Path) -> pd.DataFrame:
    """
    Transform raw EPA data into an analysis-ready dataset and save it.
    Parameters
    ----------
    raw_csv_path : Path
        Path to raw CSV file.
    processed_out_path : Path
        Path to write the processed table (parquet).
    Returns
    -------
    DataFrame
        Processed dataframe.
    """
    df = pd.read_csv(raw_csv_path, low_memory=False)

    # Standardize column names first
    df = _clean_column_names(df)

    # Type coercion and parsing
    df = _coerce_types(df)

    # Basic tidy/IDs
    df = _add_ids(df)

    # Dedupe
    df = _dedupe(df)

    # Save artifacts for EDA/testing
    _eda_artifacts(df, processed_out_path.parent.parent / "outputs")

    # Save processed
    processed_out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_parquet(processed_out_path, index=False)
    except Exception:
        # Fallback if pyarrow/fastparquet not installed
        df.to_csv(processed_out_path.with_suffix(".csv"), index=False)

    return df
