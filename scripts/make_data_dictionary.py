"""
Utility to generate a data dictionary CSV for any input CSV.
Usage:
    python scripts/make_data_dictionary.py data/extracted/EPA_Final_Data.csv data/reference-tables/data_dictionary_epa_final_data.csv
"""
import sys
import pandas as pd

def infer_dtype(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "int"
    if pd.api.types.is_float_dtype(series):
        return "float"
    if pd.api.types.is_bool_dtype(series):
        return "bool"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    return "string"

def build_dictionary(in_csv: str, out_csv: str) -> None:
    df = pd.read_csv(in_csv, low_memory=False)
    rows = []
    for col in df.columns:
        s = df[col]
        dtype = infer_dtype(s)
        n = len(s)
        n_missing = int(s.isna().sum())
        pct_missing = round(100 * n_missing / max(n, 1), 2)
        nunique = int(s.nunique(dropna=True))
        examples = s.dropna().astype(str).unique()[:3]
        rows.append({
            "column_name": col,
            "dtype_inferred": dtype,
            "n_rows": n,
            "n_unique": nunique,
            "n_missing": n_missing,
            "pct_missing": pct_missing,
            "example_values": "; ".join(examples),
            "description": ""
        })
    pd.DataFrame(rows).to_csv(out_csv, index=False)

if __name__ == "__main__":
    in_csv = sys.argv[1]
    out_csv = sys.argv[2]
    build_dictionary(in_csv, out_csv)
