import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns


mpl.rcParams['font.family'] = 'Helvetica'
mpl.rcParams['pdf.fonttype'] = 42

odds_ratios = pd.read_csv('../data/tables/figure_2H_regression_results.csv')
odds_ratios = odds_ratios.iloc[::-1].reset_index(drop = True)
odds_ratios['Color'] = odds_ratios['p'].apply(lambda x: 'navy' if x < 0.05 else '#999999')
cm = 1/2.54
fig, ax = plt.subplots(1, 1, figsize=(8*cm, 8.5*cm))


for i, row in odds_ratios.iterrows():
    ax.errorbar(
        row['estimate'],
        i,
        xerr=row['stderr'],
        fmt='o',
        capsize=2,
        capthick=0.5,
        color=row['Color'],
        linewidth=0.5,
        markersize=2
    )


ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7, linewidth = 0.5)

ax.set_yticks(range(len(odds_ratios)), odds_ratios['parm'])
ax.set_xlabel('LPM estimate on\nvideo mismatch (95% CI)', fontsize = 7, font = 'Helvetica')

ax.tick_params(axis = 'both', which = 'both', labelsize = 7)
ax.tick_params(axis = 'y', which = 'both', labelsize = 7)

sns.despine()
plt.tight_layout()

plt.savefig('../figures/figure_2H.pdf', dpi=300, bbox_inches='tight', transparent = True)
