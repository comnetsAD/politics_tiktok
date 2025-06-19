import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib as mpl
from ast import literal_eval
mpl.rcParams['pdf.fonttype'] = 42


collection_markers = {
    'overall' : 'o',
    'forYou' : 'o',
    'persona' : 'h',
}

party_colors = {
    'Republican' : 'tab:red',
    'Democrat' : 'tab:blue',
    'Neutral' : 'tab:green',
}

combined_df = pd.read_csv('../data/transcript_embeddings_projections.csv')
combined_df['embedding'] = combined_df['embedding'].apply(lambda emd: np.fromstring(emd.strip("[]"), sep=' '))

cm = 1/2.54
fig, axs = plt.subplots(1,1, figsize=(12*cm, 6*cm))

for party in combined_df['party'].unique():

    subset = combined_df[combined_df['party'] == party]
    axs.scatter(subset[subset['type'] == 'video']['x'],
                subset[subset['type'] == 'video']['y'],
                label=f"{party} video",
                color = party_colors[party],
                s = 2,
                alpha=0.05)

for party in combined_df['party'].unique():

    for collection in combined_df['collection'].unique():

        subset = combined_df[(combined_df['party'] == party) & (combined_df['collection'] == collection)]
        axs.scatter(subset[subset['type'] == 'centroid']['x'],
                    subset[subset['type'] == 'centroid']['y'],
                    marker=collection_markers[collection], s=75, edgecolors='black', linewidths=0.5,
                    label=f"{party} {collection} Centroid",
                    color = party_colors[party])

sns.despine()

axs.tick_params(axis='both', which='major', labelsize=7)
axs.set_xlabel('Dimension 1', fontsize = 7)
axs.set_ylabel('Dimension 2', fontsize = 7)

plt.xlim(-0.175, -0.05)
plt.ylim(-0.1, 0.0)

fig.savefig('../figures/figure_7C.pdf', dpi = 300, bbox_inches = 'tight', transparent = True)

dem_persona_projection = combined_df.loc[(combined_df['party'] == 'Democrat') & (combined_df['collection'] == 'persona') & (combined_df['type'] == 'centroid'), 'projection_Democrat_Republican'].values[0]
rep_persona_projection = combined_df.loc[(combined_df['party'] == 'Republican') & (combined_df['collection'] == 'persona') & (combined_df['type'] == 'centroid'), 'projection_Democrat_Republican'].values[0]
neutral_projection = combined_df.loc[(combined_df['party'] == 'Neutral') & (combined_df['collection'] == 'overall') & (combined_df['type'] == 'centroid'), 'projection_Democrat_Republican'].values[0]
print(dem_persona_projection, rep_persona_projection, neutral_projection)

fig, axs = plt.subplots(1, 1, figsize = (9*cm, 6*cm))

sns.scatterplot(y = [0, 0, 0], x = [
    dem_persona_projection,
    neutral_projection,
    rep_persona_projection,
    ], ax = axs, markers = ['h',  'o',  'h'], color = ['tab:blue', 'tab:green',  'tab:red'])

sns.despine(left = True, bottom = False)
axs.spines['left'].set_visible(False)
axs.set_yticks([0])
axs.set_yticklabels([])

axs.grid(axis = 'x', linestyle = '--', alpha = 0.15)

axs.tick_params(axis = 'both', which = 'major', labelsize = 7)

fig.savefig('../figures/figure_7D.pdf', dpi = 300, bbox_inches = 'tight', transparent = True)
