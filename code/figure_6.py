import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from datetime import datetime
import numpy as np
from ast import literal_eval
import warnings

mpl.rcParams['pdf.fonttype'] = 42
warnings.filterwarnings('ignore')

def get_group(x):
    if x == 'Anti Republican' or x == 'Pro Democrat':
        return 'Democrat'
    elif x == 'Pro Republican' or x == 'Anti Democrat':
        return 'Republican'
    elif x == 'Neutral':
        return 'Neutral'
    else:
        return None

def get_match_type(row):
    if row['leaning'] == 'left' and row['q3_majority_grouped'] == 'Republican':
        return 'left_mismatch'
    elif row['leaning'] == 'right' and row['q3_majority_grouped'] == 'Democrat':
        return 'right_mismatch'
    elif row['leaning'] == 'left' and row['q3_majority_grouped'] == 'Democrat':
        return 'left_match'
    elif row['leaning'] == 'right' and row['q3_majority_grouped'] == 'Republican':
        return 'right_match'
    # elif row['q3_majority_grouped'] == 'Neutral':
    #     return 'Neutral'
    else:
        return None

def get_rate_diff_df():
    from scipy.stats import chi2_contingency

    def get_stars(p_value):
        if p_value < 0.001:
            return '***'
        elif p_value < 0.01:
            return '**'
        elif p_value < 0.05:
            return '*'
        else:
            return ''


    from scipy.stats import chi2_contingency
    def get_test(row):
        test = chi2_contingency([[row['rep_counts'], row['rep_total_counts']], [row['dem_counts'], row['dem_total_counts']]])
        return test[1]


    topic_majority_rates = forYou_topics_dedup.groupby(['q3_majority_grouped'])['topic'].value_counts(normalize = True).reset_index()
    topic_majority_rates.columns = ['q3_majority_grouped', 'topic', 'proportion']
    topic_majority_counts = forYou_topics_dedup.groupby(['q3_majority_grouped'])['topic'].value_counts().reset_index()
    topic_majority_counts.columns = ['q3_majority_grouped', 'topic', 'count']
    topic_majority_rates = topic_majority_rates.merge(topic_majority_counts, on = ['q3_majority_grouped', 'topic'], how = 'left')


    ts = []
    rep_total_counts = []
    rep_counts = []
    dem_total_counts = []
    dem_counts = []
    diffs = []

    for i, topic in enumerate(topic_majority_rates.topic.unique()):
        ts.append(topic)
        rep_total_counts.append(topic_majority_counts.loc[(topic_majority_counts.q3_majority_grouped == 'Republican')]['count'].sum())
        rep_counts.append(topic_majority_counts.loc[(topic_majority_counts.topic == topic) & (topic_majority_counts.q3_majority_grouped == 'Republican')]['count'].values[0])
        dem_total_counts.append(topic_majority_counts.loc[(topic_majority_counts.q3_majority_grouped == 'Democrat')]['count'].sum())
        dem_counts.append(topic_majority_counts.loc[(topic_majority_counts.topic == topic) & (topic_majority_counts.q3_majority_grouped == 'Democrat')]['count'].values[0])
        diffs.append(topic_majority_rates.loc[(topic_majority_rates.topic == topic) & (topic_majority_rates.q3_majority_grouped == 'Republican')]['proportion'].values[0] - topic_majority_rates.loc[(topic_majority_rates.topic == topic) & (topic_majority_rates.q3_majority_grouped == 'Democrat')]['proportion'].values[0])


    rate_diff_df = pd.DataFrame({'topic': ts, 'rep_total_counts': rep_total_counts, 'rep_counts': rep_counts, 'dem_total_counts': dem_total_counts, 'dem_counts': dem_counts, 'diffs': diffs})
    rate_diff_df['total_counts'] = rate_diff_df['rep_counts'] + rate_diff_df['dem_counts']
    rate_diff_df = rate_diff_df.loc[rate_diff_df.total_counts > 100]
    rate_diff_df = rate_diff_df.sort_values(by = 'diffs', ascending = False).reset_index(drop = True)
    rate_diff_df['diffs'] = rate_diff_df['diffs'] * 100

    def get_color(value):
        if value < 0:
            return 'tab:blue'
        elif value > 0:
            return 'tab:red'
        else:
            return 'grey'

    diff_palette = {row['topic'] : get_color(row['diffs']) for i, row in rate_diff_df.iterrows()}

    rate_diff_df['chi_squared'] = rate_diff_df.apply(lambda row: get_test(row), axis = 1)
    rate_diff_df['stars'] = rate_diff_df['chi_squared'].apply(lambda x: '***' if x < 0.001 else ('**' if x < 0.01 else ('*' if x < 0.05 else '')))
    return rate_diff_df, diff_palette

def get_match_ratios():
    left_bots = forYou_topics.loc[forYou_topics.leaning == 'left']
    right_bots = forYou_topics.loc[forYou_topics.leaning == 'right']

    left_bots_match_ratios =left_bots.groupby('topic')['match_type'].value_counts().reset_index()
    left_bots_match_ratios.columns = ['topic', 'match_type', 'count']

    right_bots_match_ratios = right_bots.groupby('topic')['match_type'].value_counts().reset_index()
    right_bots_match_ratios.columns = ['topic', 'match_type', 'count']

    left_bots_match_ratios_pivot = left_bots_match_ratios.pivot(index = 'topic', columns = 'match_type', values = 'count').fillna(0).reset_index()
    right_bots_match_ratios_pivot = right_bots_match_ratios.pivot(index = 'topic', columns = 'match_type', values = 'count').fillna(0).reset_index()

    left_bots_match_ratios_pivot['total'] = left_bots_match_ratios_pivot['left_match'] + left_bots_match_ratios_pivot['left_mismatch']
    right_bots_match_ratios_pivot['total'] = right_bots_match_ratios_pivot['right_match'] + right_bots_match_ratios_pivot['right_mismatch']

    left_bots_match_ratios_pivot['left_match_ratio'] = left_bots_match_ratios_pivot['left_match'] / left_bots_match_ratios_pivot['total']
    right_bots_match_ratios_pivot['right_match_ratio'] = right_bots_match_ratios_pivot['right_match'] / right_bots_match_ratios_pivot['total']

    left_bots_match_ratios_pivot['left_mismatch_ratio'] = left_bots_match_ratios_pivot['left_mismatch'] / left_bots_match_ratios_pivot['total']
    right_bots_match_ratios_pivot['right_mismatch_ratio'] = right_bots_match_ratios_pivot['right_mismatch'] / right_bots_match_ratios_pivot['total']

    left_bots_match_ratios_pivot = left_bots_match_ratios_pivot.loc[left_bots_match_ratios_pivot.total > 100]
    right_bots_match_ratios_pivot = right_bots_match_ratios_pivot.loc[right_bots_match_ratios_pivot.total > 100]

    left_bots_match_ratios_pivot = left_bots_match_ratios_pivot.sort_values(by = 'left_match_ratio', ascending = True)
    right_bots_match_ratios_pivot = right_bots_match_ratios_pivot.sort_values(by = 'right_match_ratio', ascending = True)

    return left_bots_match_ratios_pivot, right_bots_match_ratios_pivot

def plot_topic_stance_difference():
    cm = 1/2.54
    fig, axs = plt.subplots(1, 1, figsize = (18*cm, 10*cm))
    sns.barplot(data = rate_diff_df, x = 'topic', y = 'diffs', ax = axs, palette = diff_palette)

    for i, row in rate_diff_df.iterrows():
        if row['diffs'] > 0:
            axs.text(x = i, y = row['diffs'] + 0.05, s = row['stars'], fontsize = 8, ha = 'center', va = 'bottom')
            axs.text(x = i, y = -0.025, s = label_map[row['topic']], fontsize = 6, ha = 'center', rotation = 90, font = 'Helvetica', va = 'top', fontweight = 'light')
        else:
            axs.text(x = i, y = row['diffs'] - 0.05, s = row['stars'], fontsize = 8, ha = 'center', va = 'top')
            axs.text(x = i, y = 0.1, s = label_map[row['topic']], fontsize = 6, ha = 'center', rotation = 90, font = 'Helvetica', va = 'bottom', fontweight = 'light')

    axs.set_xticklabels([])
    axs.set_xlabel('')
    axs.set_ylabel('Republican (%) minus Democrat (%)', fontsize = 7, font = 'Helvetica')
    axs.tick_params(bottom = False, labelsize = 7)
    sns.despine(bottom = True)
    axs.set_ylim(-5.5, 2.5)
    fig.tight_layout()
    fig.savefig('../figures/figure_6_A.pdf', dpi = 300)

def get_adjusted_label(lis):
    return_labels = []
    for x in lis:
        text = x
        if len(text) > 30:
            return_labels.append(text[:30] + '...')
        else:
            return_labels.append(text)
    return return_labels

def plot_mismatch_ratios():
    cm = 1/2.54
    fig, axs = plt.subplots(1, 2, figsize = (18 * cm, 7 * cm))

    for i, topic in enumerate(left_bots_match_ratios_pivot.topic.unique()):
        match_value = left_bots_match_ratios_pivot.loc[left_bots_match_ratios_pivot.topic == topic, 'left_match_ratio'].values[0]
        match_value = match_value * 100
        mismatch_value = left_bots_match_ratios_pivot.loc[left_bots_match_ratios_pivot.topic == topic, 'left_mismatch_ratio'].values[0]
        mismatch_value = mismatch_value * 100
        match_string = str(round(match_value, 1)) + '%'


        axs[0].barh(y = i, left = 0, width = match_value, color = 'tab:blue', alpha = 0.9)
        axs[0].barh(y = i, left = match_value, width = mismatch_value, color = 'tab:red', alpha = 0.9)
        axs[0].text(y = i, x = 1, s = match_string, fontsize = 6, ha = 'left', va = 'center', color = 'white')

    for i, topic in enumerate(right_bots_match_ratios_pivot.topic.unique()):

        match_value = right_bots_match_ratios_pivot.loc[right_bots_match_ratios_pivot.topic == topic, 'right_match_ratio'].values[0]
        match_value = match_value * 100
        mismatch_value = right_bots_match_ratios_pivot.loc[right_bots_match_ratios_pivot.topic == topic, 'right_mismatch_ratio'].values[0]
        mismatch_value = mismatch_value * 100

        match_string = str(round(match_value, 1)) + '%'

        axs[1].barh(y = i, left = 0, width = match_value, color = 'tab:red', alpha = 0.9)
        axs[1].barh(y = i, left = match_value, width = mismatch_value, color = 'tab:blue', alpha = 0.9)
        axs[1].text(y = i, x = 1, s = match_string, fontsize = 6, ha = 'left', va = 'center', color = 'white')


    axs[0].set_yticks(np.arange(len(left_bots_match_ratios_pivot.topic.unique())))
    axs[1].set_yticks(np.arange(len(right_bots_match_ratios_pivot.topic.unique())))
    axs[0].set_yticklabels(get_adjusted_label(left_bots_match_ratios_pivot.topic.unique()))
    axs[1].set_yticklabels(get_adjusted_label(right_bots_match_ratios_pivot.topic.unique()))
    axs[0].tick_params(axis = 'both', which = 'both', labelsize = 6)
    axs[1].tick_params(axis = 'both', which = 'both', labelsize = 6)
    axs[0].set_ylim(-0.5, left_bots_match_ratios_pivot.topic.nunique() - 0.1)
    axs[1].set_ylim(-0.5, right_bots_match_ratios_pivot.topic.nunique() - 0.1)

    axs[0].set_xlabel('Proportion of ideologically aligned videos', fontsize = 7, font = 'Helvetica')
    axs[1].set_xlabel('Proportion of ideologically aligned videos', fontsize = 7, font = 'Helvetica')

    sns.despine()
    fig.tight_layout()
    fig.savefig('../figures/figure_6_BC.pdf', dpi = 300, transparent=True)

forYou = pd.read_csv('../data/recommendations.csv')
topics = pd.read_csv('../data/topics.csv')

video_ids = []
video_topics = []
for i, row in topics.iterrows():
    try:
        ts = literal_eval(row['answer.topic_new'])
    except:
        continue
    for topic in ts:
        video_ids.append(row['scenario.id'])
        video_topics.append(topic)

df_t = pd.DataFrame({'video_id': video_ids, 'topic': video_topics})

forYou_topics_dedup = forYou.drop_duplicates(subset = ['video_id']).merge(df_t, on = 'video_id', how = 'left')
forYou_topics = forYou.merge(df_t, on = 'video_id', how = 'left')

forYou_topics_dedup['q3_majority_grouped'] = forYou_topics_dedup['q3_majority'].apply(lambda x: get_group(x))
forYou_topics['q3_majority_grouped'] = forYou_topics['q3_majority'].apply(lambda x: get_group(x))

rate_diff_df, diff_palette = get_rate_diff_df()

label_map = {
    'Immigration' : 'Immigration',
    'Anything outside the US or involve US foreign relations except for Israel, Gaza, Ukraine, or immigration' : 'Anything outside the US or involve US foreign relations\nexcept for Israel, Gaza, Ukraine or immigration',
    'Other social issues, including culture war issues, labor, and other social issues that are not covered above' : 'Other social issues, including culture war issues,\nlabor, and other social issues that are not covered above',
    'Crime generally' : 'Crime generally',
    'Israel, Gaza or Palestine, including anything about Netanyahu or Hamas' : 'Israel, Gaza or Palestine, including\nanything about Netanyahu or Hamas',
    'Ukraine war' : 'Ukraine war',
    'Other' : 'Other',
    'Assassination attempt on Donald Trump' : 'Assassination attempt on Donald Trump',
    'LGBTQ+ issues, including transgender issues' : 'LGBTQ+ issues, including transgender issues',
    'Other technology issues' : 'Other technology issues',
    'Covid, including covid vaccines' : 'Covid, including covid vaccines',
    'Environment generally' : 'Environment generally',
    'Government or politics generally' : 'Government or politics generally',
    'Other public health issues' : 'Other public health issues',
    'Guns and gun control' : 'Guns and gun control',
    'Racial issues, including affirmative action and racial discrimination' : 'Racial issues, including affirmative\naction and racial discrimination',
    'Democratic National Convention (DNC)' : 'Democratic National Convention',
    'Climate change' : 'Climate change',
    'Economy generally' : 'Economy generally',
    'Education' : 'Education',
    'Biden dropping out of the presidential race' : 'Biden dropping out\nof the presidential race',
    'Abortion and reproductive health' : 'Abortion and reproductive health'
}

forYou_topics['match_type'] = forYou_topics.apply(lambda row: get_match_type(row), axis = 1)

left_bots_match_ratios_pivot, right_bots_match_ratios_pivot = get_match_ratios()

plot_topic_stance_difference()
plot_mismatch_ratios()
