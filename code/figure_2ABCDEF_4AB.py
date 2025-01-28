import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib as mpl
import seaborn as sns
from datetime import datetime
import numpy as np
import warnings

warnings.filterwarnings('ignore')
mpl.rcParams['pdf.fonttype'] = 42


def get_grouping(x):
    if pd.isna(x):
        return None
    if x == 'Neutral':
        return 'Neutral'
    elif x == 'Pro Republican' or x == 'Anti Democrat':
        return 'Republican'
    elif x == 'Pro Democrat' or x == 'Anti Republican':
        return 'Democrat'
    else:
        return 'Error'

def get_alignment(df):
    # months = []
    weeks = []
    states = []
    leanings = []
    devices = []
    alignments = []
    counts = []
    
    # for month in df.month.unique():
    for week in df.week.unique():
        for state in df.state.unique():
            for leaning in df.leaning.unique():
                for device in df.device.unique():
                    try:
                        total_dem = df.loc[ (df['week'] == week) & (df['state'] == state) & (df['device'] == device) &
                                            (df['leaning'] == leaning) & (df['annotation_grouped'].isin(['Democrat']))]['count'].sum()
                    except:
                        total_dem = 0
                    try:
                        total_rep = df.loc[ (df['week'] == week) & (df['state'] == state) & (df['device'] == device) &
                                            (df['leaning'] == leaning) & (df['annotation_grouped'].isin(['Republican']))]['count'].sum()
                    except:
                        total_rep = 0
                        
                    # if total_dem == 0 and total_rep == 0:
                    #     continue
                    
                    total_all = df.loc[ (df['week'] == week) & (df['state'] == state) & (df['device'] == device) &
                                            (df['leaning'] == leaning) & (df['annotation_grouped'].isin(['Democrat', 'Republican', 'Neutral']))]['count'].sum()
                    
                    if total_all == 0:
                        continue
                    
                    alignment = ((total_rep - total_dem) / total_all)
                    
                    
                    weeks.append(week)
                    states.append(state)
                    devices.append(device)
                    leanings.append(leaning)
                    alignments.append(alignment)
                    counts.append(total_all)
                
                
    return pd.DataFrame({ 'week' : weeks, 'state': states, 'leaning': leanings, 'device': devices, 'alignment': alignments, 'num_political' : counts})

def get_skew_df(df):
    
    # months = []
    weeks = []
    states = []
    differences = []
    
    # for month in df.month.unique():
    for week in df.week.unique():
        for state in df.state.unique():
            try:
                dem_alignment = np.mean(df.loc[(df['week'] == week) & (df['state'] == state) & (df['leaning'] == 'left')]['alignment'].values)
            except:
                dem_alignment = 0
            
            try:
                rep_alignment = np.mean(df.loc[(df['week'] == week) & (df['state'] == state) & (df['leaning'] == 'right')]['alignment'].values)
            except:
                rep_alignment = 0
                
            
            
            difference = dem_alignment + rep_alignment
            
            # months.append(month)
            weeks.append(week)
            states.append(state)
            differences.append(difference)
    
    return pd.DataFrame({'week': weeks, 'state': states, 'difference': differences})

def convert_week_to_date(weeks, status = None):
    if status != None:
        print(weeks)
    dates = []
    for i in range(1, 28, 1):
        if i in weeks:
            dates.append(week_map[i][:-5])
        else:
            dates.append('')
    
    if status != None:
        print(dates)
    return dates

def get_plot_labels(state):
    if state == 'NY':
        return convert_week_to_date(ny_valid_weeks)
    elif state == 'TEXAS':
        return convert_week_to_date(texas_valid_weeks)
    else:
        return convert_week_to_date(georgia_valid_weeks)

def pad_weeks(df):
    for week in range(0, 27, 1):
        if week not in df.week.unique():
            df = pd.concat([df, pd.DataFrame({'week' : [week], 'alignment' : [None], 'leaning' : ['right']})], ignore_index = True)
            df = pd.concat([df, pd.DataFrame({'week' : [week], 'alignment' : [None], 'leaning' : ['left']})], ignore_index = True)
            df = pd.concat([df, pd.DataFrame({'week' : [week], 'alignment' : [None], 'leaning' : ['neutral']})], ignore_index = True)
            
    return df

def plot_content_figure(df, ax, state):
    
    df = pad_weeks(df)
    
    for leaning in df.leaning.unique():
        if leaning == 'right':
            
            sns.pointplot(data = df.loc[df.leaning == leaning], x = 'week', y = 'alignment', ax = ax, color = 'tab:red', 
                          marker = 'o', linewidth = 0, ms = 4, legend = False, errorbar = ('se'), err_kws={'lw' : 0.5},
                          capsize = 0.1, alpha = 0.5)
                    
            sns.regplot(data = df.loc[(df.leaning == leaning)], x = 'week', y = 'alignment',
                ax = ax, color = 'tab:red', scatter = False, order = 1, line_kws={'lw' : 1, 'ls' : '-'}, robust=True, ci = 95)
            
        elif leaning == 'left':
            sns.pointplot(data = df.loc[df.leaning == leaning], x = 'week', y = 'alignment', ax = ax, color = 'tab:blue', 
                          marker = 'o', linewidth = 0, ms = 4, legend = False, errorbar = ('se'), err_kws={'lw' : 0.5},
                          capsize = 0.1, alpha = 0.5)

            sns.regplot(data = df.loc[(df.leaning == leaning)], x = 'week', y = 'alignment', ax = ax,
                        color = 'tab:blue', scatter = False, order = 1, line_kws={'lw' : 1, 'ls' : '-'}, robust=True, ci = 95)
        
        else:
            sns.pointplot(data = df.loc[df.leaning == leaning], x = 'week', y = 'alignment', ax = ax, color = 'tab:green', 
                          marker = 'o', linewidth = 0, ms = 4, legend = False, errorbar = ('se'), err_kws={'lw' : 0.5},
                          capsize = 0.1, alpha = 0.5)        
            
            sns.regplot(data = df.loc[(df.leaning == leaning)], x = 'week', y = 'alignment', ax = ax,  color = 'tab:green', scatter = False, order = 1, line_kws={'lw' : 1, 'ls' : '-'}, robust=True, ci = 95)
    
    
    ax.set_xticks(range(0, 27, 1))
    ax.set_xticklabels([])
    ax.set_xlabel('')    

    ax.hlines(xmin = 0, xmax = 26, y = 0, linestyle = '-', color = 'black', linewidth = 0.5)
    ax.hlines(xmin = 0, xmax = 26, y = 0.5, linestyle = '-', color = 'black', linewidth = 0.25)
    ax.hlines(xmin = 0, xmax = 26, y = -0.5, linestyle = '-', color = 'black', linewidth = 0.25)
    
    ax.set_xlim(-0.5, 26.5)
    ax.set_ylim(-0.8, 0.8)
    ax.fill_between(x = [-0.5, 26.5], y1 = [0, 0], y2 = [-0.8, -0.8], color = 'tab:blue', alpha = 0.1)
    ax.fill_between(x = [-0.5, 26.5], y1 = [0, 0], y2 = [0.8, 0.8], color = 'tab:red', alpha = 0.1)

    ax.tick_params(axis = 'both', labelsize = 7)
    
    ax.set_xlabel('', fontsize = 7, font = 'Helvetica')
    if state == 'NY':
        ax.set_ylabel('Ideological content', fontsize = 7, font = 'Helvetica')
    else:
        ax.set_ylabel('', fontsize = 7, font = 'Helvetica')
    sns.despine()
    
def plot_skew_figure(df, ax, state):
    for i in range(0, 27, 1):
        if i not in df.week.unique():
            df = pd.concat([df, pd.DataFrame({'week' : [i], 'difference' : [None]})], ignore_index = True)
    
    sns.pointplot(data = df, x = 'week', y = 'difference', ax = ax, color = 'tab:orange',                  
                  marker = 'o',
                  linewidth = 0, ms = 4, legend = False, errorbar = ('ci', 95), alpha = 0.9)
    
    sns.regplot(data = df, x = 'week', y = 'difference', ax = ax, color = 'tab:orange',
                    scatter = False, order = 1, line_kws={'lw' : 1, 'ls' : '-'}, robust = True, ci = 95)
    
    ax.tick_params(axis = 'both', labelsize = 7)
    ax.set_xlabel('Week', fontsize = 7, font = 'Helvetica')
    if state == 'NY':
        ax.set_ylabel('Observed\nideological skew', fontsize = 7, font = 'Helvetica')
    else:
        ax.set_ylabel('', fontsize = 7, font = 'Helvetica')
    
    ax.set_xticklabels(get_plot_labels(state), fontsize = 5, rotation = 90, ha = 'right')  
      
    ax.hlines(xmin = 0, xmax = 26, y = 0, linestyle = '--', color = 'black', linewidth = 0.25)
    ax.set_xlim(-0.5, 26.5)
    sns.despine()
    
def generate_content_skew_figure():        
    cm = 1/2.54

    align = [alignment_df.loc[alignment_df.state == 'NY'], alignment_df.loc[alignment_df.state == 'TEXAS'], alignment_df.loc[alignment_df.state == 'GEORGIA']]
    diff = [difference_df.loc[difference_df.state == 'NY'], difference_df.loc[difference_df.state == 'TEXAS'], difference_df.loc[difference_df.state == 'GEORGIA']]

    fig, axd = plt.subplot_mosaic("""ABC
                                        DEF
                                    """, figsize = (18*cm, 10*cm), sharey = True)

    plot_content_figure(align[0], axd['A'], 'NY')
    plot_content_figure(align[1], axd['B'], 'TEXAS')
    plot_content_figure(align[2], axd['C'], 'GEORGIA')

    plot_skew_figure(diff[0], axd['D'], 'NY')
    plot_skew_figure(diff[1], axd['E'], 'TEXAS')
    plot_skew_figure(diff[2], axd['F'], 'GEORGIA')

    plt.subplots_adjust(wspace=0.05, hspace = 0.1)

    fig.savefig(f'../figures/figure_2_ABCDEF.pdf', bbox_inches = 'tight', transparent = True, dpi = 300)

def get_stance_proportions(type, ax):
    palette = {
        'Anti Democrat' : 'tab:orange',
        'Pro Democrat' : 'tab:blue',
        'Pro Republican' : 'tab:red',
        'Anti Republican' : 'lightblue',
    }
    
    sliced = forYou.loc[(forYou.leaning == type)]
    props = sliced['q3_majority'].value_counts(normalize = True).reset_index()    
    sns.barplot(data = props, x = 'proportion', y = 'q3_majority', ax = ax, palette = palette, order = ['Pro Democrat', 'Anti Republican', 'Pro Republican','Anti Democrat'])

def plot_stance_proportions():
    cm = 1/2.54
    fig, axs = plt.subplot_mosaic(""" 
                                AB
                                """, figsize = (18*cm, 4*cm), sharex = True, sharey = True)


    for letter, type in zip(['A', 'B'], ['left', 'right']):
        get_stance_proportions(type, axs[letter])

    axs['A'].set_xlabel('Proportion of political content', fontsize = 7, font = 'Helvetica')
    axs['B'].set_xlabel('Proportion of political content', fontsize = 7, font = 'Helvetica')
    axs['A'].tick_params(axis = 'both', labelsize = 7)
    axs['B'].tick_params(axis = 'both', labelsize = 7)
    axs['A'].set_ylabel('Ideological stance', fontsize = 7, font = 'Helvetica')
    sns.despine()
    plt.tight_layout()

    fig.savefig('../figures/figure_4_AB.pdf', bbox_inches = 'tight', transparent = True, dpi = 300)    
    
    
week_map = {}

for i, week in enumerate(['30-04-2024', '07-05-2024', '14-05-2024', '21-05-2024', '28-05-2024', '04-06-2024', '12-06-2024',
    '18-06-2024', '26-06-2024', '03-07-2024', '11-07-2024',
    '18-07-2024', '25-07-2024', '01-08-2024', '08-08-2024',
    '15-08-2024', '23-08-2024', '30-08-2024', '08-09-2024',
    '16-09-2024', '23-09-2024', '30-09-2024', '08-10-2024',
    '15-10-2024', '21-10-2024', '28-10-2024', '04-11-2024']):
    
    week_map[i+1] = week
    
forYou = pd.read_csv('../data/recommendations.csv')

ny_valid_weeks = []
georgia_valid_weeks = []
texas_valid_weeks = []

for week in forYou.week.unique():
    sliced = forYou.loc[forYou.week == week]
    if 'NY' in sliced.state.unique():
        ny_valid_weeks.append(week)
    if 'TEXAS' in sliced.state.unique():
        texas_valid_weeks.append(week)
    if 'GEORGIA' in sliced.state.unique():
        georgia_valid_weeks.append(week)

ny_valid_weeks = sorted([int(week) for week in ny_valid_weeks])
georgia_valid_weeks = sorted([int(week) for week in georgia_valid_weeks])
texas_valid_weeks = sorted([int(week) for week in texas_valid_weeks])

forYou['annotation_grouped'] = forYou['q3_majority'].apply(lambda x: get_grouping(x))
grouped_df = forYou.groupby(['week', 'state', 'device', 'leaning'])['annotation_grouped'].value_counts().reset_index()
alignment_df = get_alignment(grouped_df)
difference_df = get_skew_df(alignment_df)
        
        
        
generate_content_skew_figure()
plot_stance_proportions()

