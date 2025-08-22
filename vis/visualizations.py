"""
Visualization stage.

Creates exploratory and presentation-ready charts from analysis outputs.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def _plot_trend_by_year(agg_csv: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(agg_csv)
    plt.figure()
    plt.plot(df["calendar_year"], df["violations"], marker="o")
    plt.title("Total Violations by Year")
    plt.xlabel("Year")
    plt.ylabel("Violations")
    plt.tight_layout()
    plt.savefig(out_dir / "violations_trend_by_year.png", dpi=150)

def _plot_top_states(agg_csv: Path, out_dir: Path, top_n: int = 15) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(agg_csv).sort_values("violations", ascending=False).head(top_n)
    plt.figure()
    plt.bar(df["state_territory_tribe"], df["violations"])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {top_n} States by Violations")
    plt.xlabel("State/Territory/Tribe")
    plt.ylabel("Violations")
    plt.tight_layout()
    plt.savefig(out_dir / "violations_top_states.png", dpi=150)

def build_visualizations(analysis_dir: Path, vis_dir: Path) -> None:
    """
    Build default visualizations using outputs from the analysis stage.
    Parameters
    ----------
    analysis_dir : Path
        Directory containing 'agg_violations_yearly.csv' and 'agg_violations_state.csv'.
    vis_dir : Path
        Directory where figures will be saved.
    """
    yearly_csv = analysis_dir / "agg_violations_yearly.csv"
    state_csv = analysis_dir / "agg_violations_state.csv"
    figs_out = vis_dir / "figures"
    if yearly_csv.exists():
        _plot_trend_by_year(yearly_csv, figs_out)
    if state_csv.exists():
        _plot_top_states(state_csv, figs_out)
