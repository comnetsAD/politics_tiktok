import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.rcParams['font.family'] = 'Helvetica'
mpl.rcParams['pdf.fonttype'] = 42

odds_ratios = pd.read_csv('../data/regression_data/figure_4E_regression_results.csv')
odds_ratios['Color'] = odds_ratios['P-value'].apply(lambda x: 'navy' if x < 0.05 else '#999999')
cm = 1/2.54

fig, ax = plt.subplots(1, 1, figsize=(8*cm, 8*cm))


for i, row in odds_ratios.iterrows():
    ax.errorbar(
        row['Odds Ratio'],
        i,
        xerr=[[row['Odds Ratio'] - row['OR Lower CI']], 
              [row['OR Upper CI'] - row['Odds Ratio']]],
        fmt='o',
        capsize=2,
        capthick=0.5,
        color=row['Color'],
        linewidth=0.5,
        markersize=2
    )

ax.axvline(x=1, color='gray', linestyle='--', alpha=0.7, linewidth = 0.5)
ax.set_yticks(range(len(odds_ratios)), odds_ratios['Variable'])

ax.set_xlabel('Log odds ratio of\nvideo mismatch (95% CI)', fontsize = 7, font = 'Helvetica')

ax.tick_params(axis = 'both', which = 'both', labelsize = 7)
ax.tick_params(axis = 'y', which = 'both', labelsize = 6)

sns.despine()

plt.tight_layout()

plt.savefig('../figures/figure_4E.pdf', dpi=300, bbox_inches='tight', transparent = True)



