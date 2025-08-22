from pathlib import Path
import pandas as pd

def make_data_dictionary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for c in df.columns:
        s = df[c]
        rows.append({
            "variable_name": c,
            "description": "",
            "dtype": str(s.dtype),
            "missing_count": int(s.isna().sum()) if hasattr(s,'isna') else 0,
            "unique_values": int(s.nunique(dropna=True)) if hasattr(s,'nunique') else 0,
            "example": "" if s.dropna().empty else str(s.dropna().iloc[0])[:100]
        })
    return pd.DataFrame(rows)
