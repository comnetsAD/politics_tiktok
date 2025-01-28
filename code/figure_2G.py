import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42

exp_scaling = pd.read_csv('../data/model_data/full_exponential.csv')
linear_scaling = pd.read_csv('../data/model_data/full_linear.csv')
no_scaling = pd.read_csv('../data/model_data/full_none.csv')

exp_scaling = exp_scaling.groupby(['week', 'attr'])[['prop_republican', 'prop_democrat']].mean().reset_index()
linear_scaling = linear_scaling.groupby(['week', 'attr'])[['prop_republican', 'prop_democrat']].mean().reset_index()
no_scaling = no_scaling.groupby(['week', 'attr'])[['prop_republican', 'prop_democrat']].mean().reset_index()

exp_scaling['scaling'] = 'Exponential'
linear_scaling['scaling'] = 'Linear'
no_scaling['scaling'] = 'No scaling'

total_scaling = pd.concat([exp_scaling, linear_scaling,no_scaling])

forYou = pd.read_csv('../data/recommendations.csv')


def convert_to_weekly_values(df):
    weeks = []
    rep_true_values = []
    dem_true_values = []

    for week in df.week.unique():
        weeks.append(week)
        sliced = df.loc[df.week == week]
        
        try:
            pr = sliced.loc[(sliced.q3_majority == 'Pro Republican')]['proportion'].values[0]
        except:
            pr = 0
            
        try:
            ar = sliced.loc[(sliced.q3_majority == 'Anti Republican')]['proportion'].values[0]
        except:
            ar = 0
            
        try:
            prd = sliced.loc[(sliced.q3_majority == 'Pro Democrat')]['proportion'].values[0]
        except:
            prd = 0
            
        try:
            ad = sliced.loc[(sliced.q3_majority == 'Anti Democrat')]['proportion'].values[0]
        except:
            ad = 0
        
        rep_true_values.append(pr + ad)
        dem_true_values.append(prd + ar)
    
    print(weeks, rep_true_values, dem_true_values)
    df_true = pd.DataFrame({'week': weeks, 'rep_true_values': rep_true_values, 'dem_true_values': dem_true_values})
    return df_true


rep_bots = forYou.loc[(forYou.leaning == 'right') & (forYou.collection == 'forYou')  & (pd.isnull(forYou['q3_majority']) == False)].groupby(['week']).q3_majority.value_counts(normalize = True, dropna = True).reset_index()
rep_bots_true = convert_to_weekly_values(rep_bots)

dem_bots = forYou.loc[(forYou.leaning == 'left') & (forYou.collection == 'forYou') & (pd.isnull(forYou['q3_majority']) == False)].groupby(['week']).q3_majority.value_counts(normalize = True, dropna = True).reset_index()
dem_bots_true = convert_to_weekly_values(dem_bots)

rep_bots_true['difference_rep'] = rep_bots_true['rep_true_values'] - rep_bots_true['dem_true_values']
dem_bots_true['difference_dem'] = dem_bots_true['rep_true_values'] - dem_bots_true['dem_true_values']
merged_both = rep_bots_true.merge(dem_bots_true, on = 'week', how = 'left')
merged_both['alignment'] = merged_both['difference_rep'] + merged_both['difference_dem']
merged_both = merged_both[['week', 'alignment']]
merged_both['attr'] = 'Observed'
merged_both['scaling'] = 'Observed'

leanings = []
attrs = []
weeks = []
scalings = []
alignment = []

for attr in total_scaling['attr'].unique():
    for week in total_scaling['week'].unique():
        for scaling in total_scaling['scaling'].unique():
            attrs.append(attr)
            weeks.append(week)
            scalings.append(scaling)
            sliced = total_scaling.loc[(total_scaling['attr'] == attr) & (total_scaling['week'] == week) & (total_scaling['scaling'] == scaling)]

            rep_rep = sliced['prop_republican'].values.mean()
            rep_dem = sliced['prop_democrat'].values.mean()

            alignment.append(rep_rep - rep_dem)



alignment_df = pd.DataFrame({'attr': attrs, 'week': weeks, 'scaling': scalings, 'alignment': alignment})
alignment_df = pd.concat([alignment_df, merged_both])


cm = 1/2.54
fig, axs = plt.subplots(1, 1, figsize = (9*cm, 7*cm))

ax = axs
order = ['Observed', 'diggCount_zScore',  'likes_above_expected_zScore', 'commentCount_zScore', 'comments_above_expected_zScore', 'playCount_zScore', 'shareCount_zScore', 'composite_video_zScore', 'author_verified_float', 'followerCount_zScore', 'videoCount_zScore', 'heartCount_zScore', 'composite_author_zScore', 'full_composite_zScore']
label_map = {
    'diggCount_zScore': 'Likes',
    'commentCount_zScore': 'Comments',
    'likes_above_expected_zScore': 'Likes per recommendation',
    'comments_above_expected_zScore': 'Comments per recommendation',
    'playCount_zScore': 'Plays',
    'shareCount_zScore': 'Shares',
    'composite_video_zScore': 'Combined video score',
    'author_verified_float': 'Verified channel',
    'followerCount_zScore': 'Channel followers',
    'videoCount_zScore': 'Channel videos',
    'heartCount_zScore': 'Channel cumul. likes',
    'composite_author_zScore': 'Combined channel score',
    'full_composite_zScore': 'Full combined score',
    'Observed' : 'Observed',
}

sns.pointplot(data = alignment_df.loc[alignment_df.scaling == 'Observed'], x = 'attr', y = 'alignment', ax = ax, linewidth = 0, ms = 5, ci = 95, errwidth = 1, capsize = 0.1, legend = False, marker = 'D', color = 'black', errorbar='ci', order = order, alpha = 1)
sns.pointplot(data = alignment_df.loc[alignment_df.scaling == 'Linear'], x = 'attr', y = 'alignment', ax = ax, linewidth = 0, ms = 5, ci = 95, errwidth = 1, capsize = 0.1, legend = False, marker = '^', color = 'tab:purple', errorbar='ci', order = order, alpha = 0.5)
sns.pointplot(data = alignment_df.loc[alignment_df.scaling == 'Exponential'], x = 'attr', y = 'alignment', ax = ax, linewidth = 0, ms = 5, ci = 95, errwidth = 1, capsize = 0.1, legend = False, marker = 'o', color = 'tab:pink', errorbar='ci', order = order, alpha = 0.5)
sns.pointplot(data = alignment_df.loc[alignment_df.scaling == 'No scaling'], x = 'attr', y = 'alignment', ax = ax, linewidth = 0, ms = 8, ci = 95, errwidth = 1, capsize = 0.1, legend = False, marker = '*', color = 'tab:cyan', errorbar='ci', order = order, alpha = 0.5)

ax.set_ylabel('Ideological skew', fontsize = 7, font = 'Helvetica')
ax.set_xlabel('Counterfactual model attribute', fontsize = 7, font = 'Helvetica')

ax.set_xticklabels([label_map[i.get_text()] for i in ax.get_xticklabels()], fontsize = 7, rotation = 45, ha = 'right')
ax.hlines(0, -0.5, 13.5, color = 'gray', linestyle = '--', linewidth = 0.5)

ax.vlines(0.5, -0.05, 0.25, color = 'gray', linestyle = '--', linewidth = 0.5)
ax.vlines(7.5, -0.05, 0.25, color = 'gray', linestyle = '--', linewidth = 0.5)
ax.vlines(12.5, -0.05, 0.25, color = 'gray', linestyle = '--', linewidth = 0.5)
ax.set_xlim(-0.5, 13.5)
ax.set_ylim(-0.05, 0.25)
ax.tick_params(axis = 'both', which = 'both', labelsize = 7)
ax.grid(axis = 'y', color = 'gray', linestyle = '--', linewidth = 0.25, alpha = 0.25)

sns.despine()


fig.savefig('../figures/figure_2G.pdf', bbox_inches = 'tight', dpi = 300, transparent=True)


                
