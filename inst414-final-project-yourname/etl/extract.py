"""Extract stage for EPA Final Data (single CSV).
- Validates the source CSV exists in data/extracted/
- Creates an immutable raw snapshot (copied) for reproducibility
"""
from pathlib import Path
import shutil
from utils.io_helpers import EXTRACTED_DIR, ensure_dirs

SOURCE = EXTRACTED_DIR / "epa_final_data_source.csv"
RAW_SNAPSHOT = EXTRACTED_DIR / "epa_final_data_raw.csv"

def main():
    ensure_dirs()
    if not SOURCE.exists():
        raise FileNotFoundError(f"Expected {SOURCE}. Place your file there.")
    # Copy to a raw snapshot (so future transforms always use the same input)
    shutil.copy2(SOURCE, RAW_SNAPSHOT)
    print("Raw snapshot ->", RAW_SNAPSHOT)

if __name__ == "__main__":
    main()
