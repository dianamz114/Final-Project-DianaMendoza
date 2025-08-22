"""
Main entry point to run the entire project workflow.

Use:
    python main.py --run all
    python main.py --run extract
    python main.py --run transform
    python main.py --run load
    python main.py --run analysis
    python main.py --run visualize

This script orchestrates the ETL, analysis, and visualization pipeline.
"""

import argparse
from pathlib import Path

from etl.extract import extract_epa_data
from etl.transform import transform_epa_data
from etl.load import save_processed_data
from analysis.model import run_analysis_pipeline
from vis.visualizations import build_visualizations


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXTRACTED_DIR = DATA_DIR / "extracted"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = DATA_DIR / "outputs"


def main(run: str = "all") -> None:
    if run in ["all", "extract"]:
        raw_path = EXTRACTED_DIR / "EPA_Final_Data.csv"
        extract_epa_data(raw_path)

    if run in ["all", "transform"]:
        processed_path = PROCESSED_DIR / "epa_processed.parquet"
        transform_epa_data(EXTRACTED_DIR / "EPA_Final_Data.csv", processed_path)

    if run in ["all", "load"]:
        # In this scaffold, 'load' simply ensures outputs exist.
        save_processed_data(PROCESSED_DIR / "epa_processed.parquet")

    if run in ["all", "analysis"]:
        run_analysis_pipeline(PROCESSED_DIR / "epa_processed.parquet", OUTPUTS_DIR)

    if run in ["all", "visualize"]:
        build_visualizations(OUTPUTS_DIR, BASE_DIR / "vis")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the project pipeline.")
    parser.add_argument("--run", type=str, default="all",
                        help="Which stage to run: all|extract|transform|load|analysis|visualize")
    args = parser.parse_args()
    main(args.run)
