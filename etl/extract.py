"""
ETL - Extract stage.

extract by reading a local CSV in data/extracted/.
"""
from pathlib import Path
import pandas as pd

def extract_epa_data(raw_csv_path: Path) -> pd.DataFrame:
    """
    Load the raw EPA dataset from a CSV file.
    """
    df = pd.read_csv(raw_csv_path, low_memory=False)
    return df
