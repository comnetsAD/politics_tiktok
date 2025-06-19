import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from datetime import datetime
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

total = pd.read_csv('../data/regression_data/survey_regression.csv')

mpl.rcParams['font.family'] = 'Helvetica'
mpl.rcParams['pdf.fonttype'] = 42


total['Color'] = total['P-value'].apply(lambda x: 'navy' if x < 0.05 else '#999999')
cm = 1/2.54

fig, ax = plt.subplots(1, 1, figsize=(8*cm, 10*cm))

total = total.reset_index(drop = True)
total = total.iloc[::-1].reset_index(drop = True)

for i, row in total.iterrows():
    ax.errorbar(
        row['Coefficient'],
        i,
        xerr=[[row['Coefficient'] - row['Coefficient Lower CI']],
              [row['Coefficient Upper CI'] - row['Coefficient']]],
        fmt='o',
        capsize=2,
        capthick=0.5,
        color=row['Color'],
        linewidth=0.5,
        markersize=2
    )


ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7, linewidth = 0.5)
ax.set_yticks(range(len(total)), total['Variable'])
ax.set_xlabel('Republican respondents \ncompared to Democratic respondents', fontsize = 7, font = 'Helvetica')
ax.tick_params(axis = 'both', which = 'both', labelsize = 7)
ax.tick_params(axis = 'y', which = 'both', labelsize = 7)
ax.set_xlim(-2, 2)

sns.despine(left = True)
plt.tight_layout()

plt.savefig('../figures/figure_5.pdf', dpi=300, bbox_inches='tight', transparent = True)
