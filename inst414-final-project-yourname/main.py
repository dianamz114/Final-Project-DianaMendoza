"""Entry point for the EPA Final Data pipeline.
Usage:
  python main.py --stage all
  python main.py --stage extract|transform|model|evaluate|vis
"""
import argparse
from etl.extract import main as extract_main
from etl.transform import main as transform_main
from analysis.model import train_and_log
from analysis.evaluate import export_predictions, sweep_thresholds
from vis.visualizations import violations_by_year_type

def run_all():
    extract_main()
    transform_main()
    train_and_log()
    export_predictions('rf', 0.5)
    sweep_thresholds('rf')
    violations_by_year_type()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', choices=['all','extract','transform','model','evaluate','vis'], default='all')
    args = ap.parse_args()
    if args.stage == 'all':
        run_all()
    elif args.stage == 'extract':
        extract_main()
    elif args.stage == 'transform':
        transform_main()
    elif args.stage == 'model':
        train_and_log()
    elif args.stage == 'evaluate':
        export_predictions('rf', 0.5); sweep_thresholds('rf')
    elif args.stage == 'vis':
        violations_by_year_type()

if __name__ == '__main__':
    main()
