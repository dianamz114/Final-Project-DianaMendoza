"""
ETL - Load stage.

For this class project, "load" persists the processed dataset.
If you integrate with databases or data warehouses later, swap the sink here.
"""
from pathlib import Path

def save_processed_data(processed_path: Path) -> None:
    """
    Verifies that the processed dataset exists and is readable.
    Parameters
    ----------
    processed_path : Path
        Path to the processed file (.parquet or .csv fallback).
    """
    # In a real pipeline, you might copy to a warehouse, S3, etc.
    # For now, we simply check existence.
    if not processed_path.exists() and not processed_path.with_suffix(".csv").exists():
        raise FileNotFoundError(f"Processed data not found at {processed_path} or CSV fallback.")
