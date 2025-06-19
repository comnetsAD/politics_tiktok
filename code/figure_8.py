import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import pandas as pd
import matplotlib as mpl


rates_df = pd.read_csv('../data/transcript_availability_analysis.csv')

mpl.rcParams['pdf.fonttype'] = 42

palette = {
    True : 'tab:orange',
    False : 'tab:purple'
}

cm = 1/2.54
fig, axs = plt.subplots(1, 2, figsize = (18*cm, 10*cm), sharey = True)
sns.barplot(data = rates_df.loc[rates_df.bot_type == 'Democrat'], x = 'video_type', y = 'percentage', hue = 'is_transcript',   ax = axs[0], palette = palette, order = ['Political', 'Election', 'Neutral', 'Democrat', 'Republican'], legend = True)
sns.barplot(data = rates_df.loc[rates_df.bot_type == 'Republican'], x = 'video_type', y = 'percentage', hue = 'is_transcript', ax = axs[1], palette = palette, order = ['Political', 'Election', 'Neutral', 'Democrat', 'Republican'], legend = False)

axs[0].set_ylim(0, 1)


for i in range(2):
    axs[i].set_xlabel('Video Type', fontsize = 7)
    axs[i].set_ylabel('Proportion of Videos', fontsize = 7)
    axs[i].tick_params(axis = 'both', labelsize = 7)

axs[0].set_title('Democrat bots', fontsize = 7)
axs[1].set_title('Republican bots', fontsize = 7)

sns.despine()

fig.savefig('../figures/figure_8.pdf', bbox_inches = 'tight', dpi = 300, transparent = True)
