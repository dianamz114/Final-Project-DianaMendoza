from pathlib import Path
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, average_precision_score,
                             RocCurveDisplay, PrecisionRecallDisplay)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from utils.io_helpers import PROCESSED_DIR, OUTPUTS_DIR

def load_xy():
    df = pd.read_csv(PROCESSED_DIR/'model_ready.csv')
    X = df.drop(columns=['pws_id','high_risk_label'], errors='ignore')
    y = df['high_risk_label'].astype(int)
    return X, y

def train_and_log():
    X, y = load_xy()
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    models = {
        'logit': LogisticRegression(max_iter=1000, class_weight='balanced'),
        'rf': RandomForestClassifier(n_estimators=300, class_weight='balanced_subsample', random_state=42)
    }
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR/'figures').mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR/'models').mkdir(parents=True, exist_ok=True)
    (OUTPUTS_DIR/'metrics').mkdir(parents=True, exist_ok=True)

    results = {}
    for name, mdl in models.items():
        mdl.fit(X_tr, y_tr)
        prob = mdl.predict_proba(X_te)[:,1]
        pred = (prob >= 0.5).astype(int)

        # metrics
        roc = roc_auc_score(y_te, prob)
        ap = average_precision_score(y_te, prob)
        rep = classification_report(y_te, pred, digits=3)
        cm = confusion_matrix(y_te, pred)

        # curves
        RocCurveDisplay.from_predictions(y_te, prob)
        plt.title(f'{name.upper()} – ROC')
        plt.savefig(OUTPUTS_DIR/'figures'/f'{name}_roc.png', bbox_inches='tight')
        plt.close()

        PrecisionRecallDisplay.from_predictions(y_te, prob)
        plt.title(f'{name.upper()} – Precision-Recall')
        plt.savefig(OUTPUTS_DIR/'figures'/f'{name}_pr.png', bbox_inches='tight')
        plt.close()

        # save model + log
        joblib.dump(mdl, OUTPUTS_DIR/'models'/f'{name}.joblib')
        results[name] = {
            'roc_auc': float(roc),
            'avg_precision': float(ap),
            'report': rep,
            'confusion_matrix': cm.tolist()
        }

    with open(OUTPUTS_DIR/'metrics'/'model_metrics.json', 'w') as f:
        json.dump(results, f, indent=2)

    print('Saved models, metrics, and figures to data/outputs/')

if __name__ == '__main__':
    train_and_log()
