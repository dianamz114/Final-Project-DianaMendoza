from pathlib import Path

DATA_DIR = Path('data')
EXTRACTED_DIR = DATA_DIR / 'extracted'
PROCESSED_DIR = DATA_DIR / 'processed'
OUTPUTS_DIR = DATA_DIR / 'outputs'
REF_DIR = DATA_DIR / 'reference-tables'

def ensure_dirs():
    for p in [DATA_DIR, EXTRACTED_DIR, PROCESSED_DIR, OUTPUTS_DIR, REF_DIR]:
        p.mkdir(parents=True, exist_ok=True)
