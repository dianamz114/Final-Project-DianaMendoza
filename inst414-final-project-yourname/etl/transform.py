"""Transform stage for EPA Final Data.
- Standardizes columns
- Builds facility-year and facility-level aggregates
- Creates a binary high_risk_label
- Writes processed outputs
- Emits basic EDA CSVs to outputs/metrics/
"""
from pathlib import Path
import pandas as pd
import numpy as np
from utils.io_helpers import EXTRACTED_DIR, PROCESSED_DIR, OUTPUTS_DIR, ensure_dirs

RAW = EXTRACTED_DIR / "epa_final_data_raw.csv"

COLUMN_MAP = {
    'PWS ID': 'pws_id',
    'PWS Name': 'pws_name',
    'Detailed Facility Report': 'detail_url',
    'Calendar Year': 'calendar_year',
    'Primacy Agency Type': 'primacy',
    'State/Territory/Tribe': 'state_or_tribe',
    'City Served': 'city',
    'Population Served': 'population_served',
    'Water System Type': 'system_type',
    'System Size': 'system_size',
    'Source Water': 'source_water',
    'Violation Type': 'violation_type',
    'Violations': 'violations'
}

def standardize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={c: COLUMN_MAP.get(c, c) for c in df.columns})
    keep = list(COLUMN_MAP.values())
    cols = [c for c in keep if c in df.columns]
    df = df[cols].copy()
    # Types
    if 'calendar_year' in df.columns:
        df['calendar_year'] = pd.to_numeric(df['calendar_year'], errors='coerce').astype('Int64')
    if 'population_served' in df.columns:
        df['population_served'] = pd.to_numeric(df['population_served'].astype(str).str.replace(',',''), errors='coerce')
    if 'violations' in df.columns:
        df['violations'] = pd.to_numeric(df['violations'], errors='coerce').fillna(0).astype(int)
    return df

def make_facility_year(df: pd.DataFrame) -> pd.DataFrame:
    fy = df.dropna(subset=['calendar_year']).copy()
    fy['calendar_year'] = fy['calendar_year'].astype('Int64')
    return fy

def aggregate_facility(fy: pd.DataFrame) -> pd.DataFrame:
    max_year = fy['calendar_year'].dropna().max()
    window = {max_year, max_year-1, max_year-2} if pd.notna(max_year) else set()

    # By violation type
    if 'violation_type' in fy.columns:
        pivot_vt = (fy.pivot_table(index='pws_id', columns='violation_type',
                                   values='violations', aggfunc='sum', fill_value=0)
                    .add_prefix('vt_').reset_index())
    else:
        pivot_vt = fy.groupby('pws_id', as_index=False)['violations'].sum().rename(columns={'violations':'vt_all'})

    grp = fy.groupby('pws_id', as_index=False).agg(
        total_violations=('violations','sum'),
        years_reported=('calendar_year', lambda s: s.dropna().nunique())
    )

    if window:
        last3 = (fy[fy['calendar_year'].isin(list(window))]
                 .groupby('pws_id', as_index=False)['violations'].sum()
                 .rename(columns={'violations':'violations_last3'}))
    else:
        last3 = grp[['pws_id']].assign(violations_last3=np.nan)

    cat_cols = [c for c in ['pws_name','primacy','state_or_tribe','city','system_type','system_size','source_water'] if c in fy.columns]
    recent = (fy.sort_values(['pws_id','calendar_year'])
                .groupby('pws_id')[cat_cols]
                .tail(1).reset_index(drop=True))

    fac = grp.merge(last3, on='pws_id', how='left')\
             .merge(pivot_vt, on='pws_id', how='left')\
             .merge(recent, on='pws_id', how='left')

    if 'population_served' in fy.columns:
        fac['population_served'] = (fy.sort_values(['pws_id','calendar_year'])
                                      .groupby('pws_id')['population_served']
                                      .tail(1).reset_index(drop=True))

    for col in ['system_type','system_size','source_water','primacy']:
        if col in fac.columns:
            dummies = pd.get_dummies(fac[col], prefix=col, dummy_na=True)
            fac = pd.concat([fac, dummies], axis=1)

    # Label definition (adjustable): >= 3 violations in last 3 years OR total >= 3
    thr = 3
    fac['high_risk_label'] = ((fac['violations_last3'].fillna(0) >= thr) | (fac['total_violations'] >= thr)).astype(int)

    return fac

def basic_eda(fy: pd.DataFrame):
    (OUTPUTS_DIR/'metrics').mkdir(parents=True, exist_ok=True)
    fy.describe(include='all').to_csv(OUTPUTS_DIR/'metrics'/'eda_facility_year_describe.csv')
    if 'violation_type' in fy.columns:
        (fy.groupby(['calendar_year','violation_type'])['violations'].sum()
           .reset_index()
           .to_csv(OUTPUTS_DIR/'metrics'/'violations_by_year_type.csv', index=False))

def main():
    ensure_dirs()
    if not RAW.exists():
        raise FileNotFoundError(f"Missing {RAW}. Run etl/extract.py first.")
    df = pd.read_csv(RAW, low_memory=False)
    std = standardize(df)
    fy = make_facility_year(std)
    basic_eda(fy)
    fac = aggregate_facility(fy)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    (PROCESSED_DIR/'merged_yearly.csv').write_text('')  # ensure file exists even if empty? We'll write real data
    fy.to_csv(PROCESSED_DIR/'merged_yearly.csv', index=False)
    fac.to_csv(PROCESSED_DIR/'facility_agg.csv', index=False)

    # model-ready
    target = 'high_risk_label'
    drop_cols = ['pws_name','city','state_or_tribe']
    features = fac.drop(columns=[c for c in drop_cols if c in fac.columns], errors='ignore')
    feat_cols = [c for c in features.columns if c == 'pws_id' or pd.api.types.is_numeric_dtype(features[c])]
    model_df = features[feat_cols].copy()
    model_df.to_csv(PROCESSED_DIR/'model_ready.csv', index=False)

    print('Processed ->', PROCESSED_DIR/'merged_yearly.csv')
    print('Processed ->', PROCESSED_DIR/'facility_agg.csv')
    print('Processed ->', PROCESSED_DIR/'model_ready.csv')

if __name__ == "__main__":
    main()
