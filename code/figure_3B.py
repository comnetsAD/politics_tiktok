import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_filter_data(recommendations_data, videos_data):
    """Load input CSV and filter based on specific conditions."""
    recommendations_df = pd.read_csv(recommendations_data)
    recommendations_df = recommendations_df.loc[recommendations_df['leaning'] != 'neutral']
    videos_df = pd.read_csv(videos_data)
    recommendations_with_authors_df = pd.merge(recommendations_df, videos_df[['video_id', 'author_uniqueId']], on='video_id', how='inner')
    return recommendations_with_authors_df


def compute_mismatch(input_df):
    mismatch_data = []
    MIN_COUNT_THRESHOLD = 10

    for state, group in input_df.groupby(['state']):
        # Process right-leaning channels
        for channel in republican_candidates:
            total = len(group.loc[group['author_uniqueId'] == channel])
            if total >= MIN_COUNT_THRESHOLD:
                mismatch = len(group.loc[(group['author_uniqueId'] == channel) & (group['leaning'] == 'left')]) / total
                mismatch_data.append({
                    "author_uniqueId": channel, 
                    "mismatch": mismatch, "count": total, "state": state, "party": "Republican"
                })

        # Process left-leaning channels
        for channel in democrat_candidates:
            total = len(group.loc[group['author_uniqueId'] == channel])
            if total >= MIN_COUNT_THRESHOLD:
                mismatch = len(group.loc[(group['author_uniqueId'] == channel) & (group['leaning'] == 'right')]) / total
                mismatch_data.append({
                    "author_uniqueId": channel,
                    "mismatch": mismatch, "count": total, "state": state, "party": "Democrat"
                })
    return pd.DataFrame(mismatch_data)

# Plot mismatch data
def plot_mismatch(mismatch_df, party_cmap, output_file):
    FIGURE_DPI = 300
    FIGURE_SIZE_CM = (5 / 2.54, 3 / 2.54)  # Convert from cm to inches
    LABEL_SIZE_CM = 15 / 2.54
    FONT_SIZE_CM = 10 / 2.54

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_CM, dpi=FIGURE_DPI)
    sns.boxplot(data=mismatch_df, y='party', x='mismatch', width=0.4, showfliers=False,showmeans =True, meanprops = {'mfc': 'yellow', 'mec': 'black', 'ms': 2.5, 'mew': 0.5},  order=['Republican', 'Democrat'], palette=party_cmap, linewidth=0.5)

    ax.tick_params(axis='x', rotation=0, labelsize=LABEL_SIZE_CM)
    ax.tick_params(axis='y', labelsize=LABEL_SIZE_CM)
    ax.set_xlabel('Mismatch Proportion', fontsize=LABEL_SIZE_CM)
    ax.set_ylabel('', fontsize=FONT_SIZE_CM)
    sns.despine()

    for label in ax.get_yticklabels():
        label.set_color(party_cmap[label.get_text()])
        label.set_fontsize(FONT_SIZE_CM)

    plt.tight_layout(pad=0.5)
    fig.savefig(output_file)

# Constants
OUTPUT_FILE = "../figures/figure_3B.pdf"
RECOMMENDATION_DATA = "../data/recommendations.csv"
VIDEO_DATA = "../data/top_channel_videos.csv"

democrat_candidates = ["kamalaharris", "kamalahq", "timwalz"]
republican_candidates = ["teamtrump", "realdonaldtrump","jd"]
candidates = democrat_candidates + republican_candidates
party_cmap = {'Republican': 'tab:red', 'Democrat': 'tab:blue'}


df = load_and_filter_data(RECOMMENDATION_DATA, VIDEO_DATA)
mismatch_df = compute_mismatch(df)
plot_mismatch(mismatch_df, party_cmap, OUTPUT_FILE)