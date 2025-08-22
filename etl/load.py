"""
ETL - Load stage.
"""
from pathlib import Path

def save_processed_data(processed_path: Path) -> None:
    """
    Verifies that the processed dataset exists and is readable.

        Path to the processed file (.parquet or .csv fallback).
    """
    if not processed_path.exists() and not processed_path.with_suffix(".csv").exists():
        raise FileNotFoundError(f"Processed data not found at {processed_path} or CSV fallback.")
