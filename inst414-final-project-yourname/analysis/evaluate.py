from pathlib import Path
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import precision_recall_curve
from utils.io_helpers import PROCESSED_DIR, OUTPUTS_DIR

def export_predictions(model_name='rf', threshold=0.5):
    df = pd.read_csv(PROCESSED_DIR/'model_ready.csv')
    X = df.drop(columns=['pws_id','high_risk_label'], errors='ignore')
    mdl = joblib.load(OUTPUTS_DIR/'models'/f'{model_name}.joblib')
    prob = mdl.predict_proba(X)[:,1]
    pred = (prob >= threshold).astype(int)
    out = df[['pws_id']].copy()
    out['prob_high_risk'] = prob
    out['pred_high_risk'] = pred
    out.to_csv(OUTPUTS_DIR/f'{model_name}_predictions.csv', index=False)
    print('Wrote', OUTPUTS_DIR/f'{model_name}_predictions.csv')

def sweep_thresholds(model_name='rf'):
    df = pd.read_csv(PROCESSED_DIR/'model_ready.csv')
    X = df.drop(columns=['pws_id','high_risk_label'], errors='ignore')
    y = df['high_risk_label'].astype(int)
    mdl = joblib.load(OUTPUTS_DIR/'models'/f'{model_name}.joblib')
    prob = mdl.predict_proba(X)[:,1]
    p, r, t = precision_recall_curve(y, prob)
    pr = pd.DataFrame({'precision': p[:-1], 'recall': r[:-1], 'threshold': t})
    pr.to_csv(OUTPUTS_DIR/f'{model_name}_pr_thresholds.csv', index=False)
    print('Wrote', OUTPUTS_DIR/f'{model_name}_pr_thresholds.csv')

if __name__ == '__main__':
    export_predictions('rf', 0.5)
    sweep_thresholds('rf')
