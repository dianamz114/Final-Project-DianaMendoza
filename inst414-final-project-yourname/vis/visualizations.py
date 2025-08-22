import pandas as pd
import matplotlib.pyplot as plt
from utils.io_helpers import PROCESSED_DIR, OUTPUTS_DIR

def violations_by_year_type():
    df = pd.read_csv(PROCESSED_DIR/'merged_yearly.csv')
    if not {'calendar_year','violations','violation_type'}.issubset(df.columns):
        print('Missing columns for plot.')
        return
    plot_df = df.groupby(['calendar_year','violation_type'])['violations'].sum().reset_index()
    for vt, grp in plot_df.groupby('violation_type'):
        grp = grp.sort_values('calendar_year')
        plt.plot(grp['calendar_year'], grp['violations'], label=str(vt))
    plt.xlabel('Calendar Year'); plt.ylabel('Violations')
    plt.title('Violations by Year and Type')
    plt.legend()
    out = OUTPUTS_DIR/'figures'/'violations_by_year_type.png'
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print('Saved', out)

if __name__ == '__main__':
    violations_by_year_type()
