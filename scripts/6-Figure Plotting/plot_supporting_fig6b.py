import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns

from matplotlib import colormaps, cm
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from pandas.plotting import parallel_coordinates

from helper_parallel_plot_functions import *
from helper_functions_robustness import *

# setup attributes
sim_mode = 'p90'
num_sol_dict = {'base': 46, 'IU': 628}
yticks_max = {'avg': [0.0, 0.5, 1.0], 'p90': [0.0, 0.45, 0.90]}
sim_mode_colors = {'base': '#6B8F71', 'IU': '#F2B880'}
utilities = ['Watertown', 'Dryville', 'Fallsland']
util_abbrevs = ['W', 'D', 'F']
obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
objs_allutils = [obj_name + f'_{util_abbrev}' for util_abbrev in util_abbrevs for obj_name in obj_names]
objs_regional = [obj_name + '_R' for obj_name in obj_names]

high_coop_base_solutions = 29 
high_coop_IU_solutions = 401

# read in the robustness dataframes from csv
robustness_df_avg = pd.read_csv(f'robustness_sim_avg_refset_base.csv')
robustness_df_p90 = pd.read_csv(f'robustness_sim_p90_refset_base.csv')

robustness_df_avg['Category'] = 'other'
robustness_df_p90['Category'] = 'other'

robustness_df_avg['Category'] = ['avg' if i in [high_coop_base_solutions[0]] else 'other' for i in robustness_df_avg.index]
robustness_df_p90['Category'] = ['p90' if i in [high_coop_base_solutions[0]] else 'other' for i in robustness_df_p90.index]

robustness_df_avg.loc[high_coop_base_solutions[0], 'Category'] = 'avg'
robustness_df_p90.loc[high_coop_base_solutions[0], 'Category'] = 'p90'

robustness_base_avg = pd.DataFrame(robustness_df_avg.iloc[high_coop_base_solutions[0]])
robustness_base_p90 = pd.DataFrame(robustness_df_p90.iloc[high_coop_base_solutions[0]])
# drop the regional column for plotting
robustness_df_avg_noReg = robustness_df_avg.drop(columns=['Regional'])
robustness_df_p90_noReg = robustness_df_p90.drop(columns=['Regional'])
color_dict_coop_bavg = {'other': "#E6E6E6", 'avg': "#83C78D", 'p90': "#39563D"}

fig, ax = plt.subplots(1,1,figsize=(10,4), gridspec_kw={'hspace':0.1, 'wspace':0.1})
axis_labels = ['Watertown', 'Dryville', 'Fallsland'] 
figname_base = f'robustness_parallel_base_avg_p90'
axis_mins = [0.2, 0.2, 0.2]
axis_maxs = [1.0, 1.0, 1.0]

custom_parallel_coordinates(fig, ax, robustness_df_avg_noReg, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='top', zorder_by=2,
                                alpha_base=0.5, lw_base=1.0, fontsize=14,
                                minmaxs=['max', 'max', 'max'],
                                color_by_categorical='Category',
                                color_dict_categorical=color_dict_coop_bavg,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 
                                
custom_parallel_coordinates(fig, ax, robustness_base_avg, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='top', 
                                alpha_base=0.85, lw_base=5, fontsize=14,
                                minmaxs=['max', 'max', 'max'],
                                color_by_categorical='Category',
                                color_dict_categorical=color_dict_coop_bavg,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

custom_parallel_coordinates(fig, ax, robustness_base_p90, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='top', 
                                alpha_base=0.85, lw_base=4, fontsize=14,
                                minmaxs=['max', 'max', 'max'],
                                color_by_categorical='Category',
                                color_dict_categorical=color_dict_coop_bavg,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

plt.title(f'Robustness of high coop base solution under avg and p90 conditions', fontsize=16)
plt.savefig(f'supporting_fig6b.pdf', bbox_inches='tight', dpi=300)
plt.show()