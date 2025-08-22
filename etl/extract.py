"""
ETL - Extract stage.

For Part 2, we "extract" by reading a local CSV that you placed in data/extracted/.
Later you could swap this with a web/API/database extractor and leave the interface the same.
"""
from pathlib import Path
import pandas as pd

def extract_epa_data(raw_csv_path: Path) -> pd.DataFrame:
    """
    Load the raw EPA dataset from a CSV file.
    Parameters
    ----------
    raw_csv_path : Path
        Path to the raw CSV in data/extracted/.
    Returns
    -------
    DataFrame
        Raw dataframe as-is (no cleaning).
    """
    df = pd.read_csv(raw_csv_path, low_memory=False)
    # Save a lightweight proof-of-extraction artifact if desired
    (raw_csv_path.parent / "EXTRACTION_OK.txt").write_text("Raw data present and readable.")
    return df
