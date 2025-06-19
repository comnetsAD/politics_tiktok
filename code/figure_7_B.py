import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/seeding_comments_annotated.csv')
rates = df.groupby(['video_grouped', 'scenario.vid'])['comment_grouped'].value_counts(normalize = True).reset_index()

mpl.rcParams['pdf.fonttype'] = 42

cm = 1/2.54

fig, axs = plt.subplots(1,1, figsize = (9*cm, 6*cm))

sns.barplot(data = rates.loc[rates.video_grouped != 'Neutral'], y = 'video_grouped', x = 'proportion', hue = 'comment_grouped', ax = axs, palette = {
    'Democrat' : 'tab:blue',
    'Republican' : 'tab:red',
    'Neutral' : 'tab:green',
}, capsize=0.25, errwidth = 1, legend = False)

axs.set_xlabel('Proportion of comments', fontsize = 7)
axs.set_ylabel('Video partisanship', fontsize = 7)
axs.set_xticklabels(axs.get_xticklabels(), fontsize = 7)
axs.set_yticklabels(axs.get_yticklabels(), fontsize = 7)

sns.despine()
fig.savefig('../figures/figure_7B.pdf', dpi = 300, bbox_inches = 'tight', transparent = True)
