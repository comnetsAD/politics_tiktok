import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess data
def load_and_filter_data(recommendations_data, videos_data):
    """Load input CSV and filter based on specific conditions."""
    recommendations_df = pd.read_csv(recommendations_data)
    recommendations_df = recommendations_df.loc[recommendations_df['leaning'] != 'neutral']
    videos_df = pd.read_csv(videos_data)
    recommendations_with_authors_df = pd.merge(recommendations_df, videos_df[['video_id', 'author_uniqueId']], on='video_id', how='inner')
    return recommendations_with_authors_df

# Create a color map for authors
def create_author_color_map():
    """Create a dictionary mapping each channel to its respective color."""
    leaning_cmap = {"right": "tab:red", "left": "tab:blue"}
    author_cmap = {}
    for channel in RIGHT_CHANNELS:
        author_cmap[channel] = leaning_cmap['right']
    for channel in LEFT_CHANNELS:
        author_cmap[channel] = leaning_cmap['left']
    return author_cmap


def compute_mismatch(input_df):
    """Calculate mismatch ratios for left and right channels grouped by state."""
    mismatch_data = []
    MIN_COUNT_THRESHOLD = 10

    for state, group in input_df.groupby(['state']):
        # Process right-leaning channels
        for channel in RIGHT_CHANNELS:
            total = len(group.loc[group['author_uniqueId'] == channel])
            if total >= MIN_COUNT_THRESHOLD:
                mismatch = len(group.loc[(group['author_uniqueId'] == channel) & (group['leaning'] == 'left')]) / total
                mismatch_data.append({
                    "author_uniqueId": channel, "leaning": "right",
                    "mismatch": mismatch, "count": total, "state": state
                })

        # Process left-leaning channels
        for channel in LEFT_CHANNELS:
            total = len(group.loc[group['author_uniqueId'] == channel])
            if total >= MIN_COUNT_THRESHOLD:
                mismatch = len(group.loc[(group['author_uniqueId'] == channel) & (group['leaning'] == 'right')]) / total
                mismatch_data.append({
                    "author_uniqueId": channel, "leaning": "left",
                    "mismatch": mismatch, "count": total, "state": state
                })

    return pd.DataFrame(mismatch_data)

# Plot mismatch data
def plot_mismatch(mismatch_df, author_cmap, output_file):    
    FIGURE_DPI = 300
    FIGURE_SIZE_CM = (9 / 2.54, 10 / 2.54)  # Convert from cm to inches
    LABEL_SIZE_CM = 15 / 2.54
    FONT_SIZE_CM = 12 / 2.54

    authors_ordered = mismatch_df.groupby('author_uniqueId')['mismatch'].mean().sort_values(ascending=False).index.tolist()

    fig, ax = plt.subplots(1,1, figsize=FIGURE_SIZE_CM, dpi=FIGURE_DPI)
    sns.boxplot(
        data=mismatch_df, y='author_uniqueId', x='mismatch',
        width=0.4, hue='author_uniqueId', showfliers=False, showmeans=True,
        meanprops={'mfc': 'yellow', 'mec': 'black', 'ms': 3, 'mew': 0.5},
        order=authors_ordered, palette=author_cmap, linewidth=0.5
    )

    # Customize axes and labels
    ax.tick_params(axis='x', rotation=0, labelsize=LABEL_SIZE_CM)
    ax.tick_params(axis='y', labelsize=LABEL_SIZE_CM)
    ax.set_xlabel('Mismatch Proportion', fontsize=LABEL_SIZE_CM)
    ax.set_ylabel('', fontsize=FONT_SIZE_CM)
    sns.despine()

    # Set y-axis tick colors
    for label in ax.get_yticklabels():
        label.set_color(author_cmap[label.get_text()])
        label.set_fontsize(FONT_SIZE_CM)

    plt.tight_layout(pad=0.5)
    fig.savefig(output_file, dpi=FIGURE_DPI, bbox_inches='tight')


# Constants
OUTPUT_FILE = "../figures/figure_3A.pdf"
RECOMMENDATION_DATA = "../data/recommendations.csv"
VIDEO_DATA = "../data/top_channel_videos.csv"

# Top Democrat Channels by followers
LEFT_CHANNELS = [
    "kamalaharris", "tizzyent", "kamalahq", "msnbc", "nowthisimpact", "theviewabc",
    "colbertlateshow", "jeffjacksonnc", "timwalz", "jimmykimmellive", "bernie",
    "harryjsisson", "thedemocrats", "couriernewsroom", "aaronparnas1", "nytimes",
    "meidastouch", "aocinthehouse", "rbreich", "latenightseth"
]
# Top Republican Channels by followers
RIGHT_CHANNELS = [
    "realdonaldtrump", "teamtrump", "thecharliekirkshow", "daterightstuff", "candaceoshow",
    "robertfkennedyjrofficial", "adamcalhoun1", "real.benshapiro", "jd",
    "piersmorganuncensored", "tuckercarlson", "foxnews", "thecommentssectiondw",
    "the_jefferymead", "donaldjtrumpjr", "charliekirkdebateclips", "maga",
    "theofficertatum", "jessebwatters", "patrickbetdavid"
]

df = load_and_filter_data(RECOMMENDATION_DATA, VIDEO_DATA)
mismatch_df = compute_mismatch(df)
author_cmap = create_author_color_map()
plot_mismatch(mismatch_df, author_cmap, OUTPUT_FILE)