import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42

total = pd.read_csv('../data/seeding_video_type_rates.csv')

palette = {
    'left' : 'tab:blue',
    'right' : 'tab:red',
}

cm = 1/2.54
fig, axs = plt.subplots(1, 1, figsize = (9*cm, 6*cm))

sns.barplot(y = 'video_type', x = 'proportion', hue = 'leaning', data = total, palette = palette, ax = axs, legend = False, capsize = 0.25, errwidth = 1)

axs.set_xlabel('Rate', fontsize = 7)
axs.set_ylabel('Video Type', fontsize = 7)
axs.set_yticklabels(['Election-Related', 'Positive Partisanship', 'Negative Partisanship', 'Neutral Videos'], fontsize = 7)
axs.tick_params(axis = 'both', which = 'major', labelsize = 7)
sns.despine()

fig.savefig('../figures/figure_7A.pdf', dpi = 300, bbox_inches = 'tight', transparent = True)
