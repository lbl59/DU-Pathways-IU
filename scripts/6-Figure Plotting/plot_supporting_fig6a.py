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
robustness_df_IU = pd.read_csv(f'robustness_sim_{sim_mode}_refset_IU.csv')
robustness_df_base = pd.read_csv(f'robustness_sim_{sim_mode}_refset_base.csv')

sols_to_highlight = {"baseline": high_coop_base_solutions,
                     "IU social planner": high_coop_IU_solutions}

# maintain only IU solutions that have higher regional robustness than their counterparts in the base set
robustness_df_IU_higherthanbase = robustness_df_IU[robustness_df_IU['Regional'] > robustness_df_base['Regional'].median()]
robustness_df_IU_idx = robustness_df_IU_higherthanbase.index.tolist()

color_dict_coop = {'other': "#E6E6E6", 'base': "#39563D", 'IU social planner': "#B66D0D"}
robustness_df_base_cat = robustness_df_base.copy()
robustness_df_IU_cat = robustness_df_IU.copy()
robustness_df_base_cat['Category'] = 'other'
robustness_df_IU_cat['Category'] = 'other'

robustness_df_base_cat['Category'] = ['base' if i in [high_coop_base_solutions[0]] else 'other' for i in robustness_df_base_cat.index]
robustness_df_IU_cat['Category'] = ['IU social planner' if i in [high_coop_IU_solutions[0]] else 'other' for i in robustness_df_IU_cat.index]

robustness_IU_highcoop = pd.DataFrame(robustness_df_IU_cat.iloc[high_coop_IU_solutions[0]])
robustness_base_highcoop = pd.DataFrame(robustness_df_base_cat.iloc[high_coop_base_solutions[0]])

robustness_IU_cat = pd.concat([robustness_df_IU_cat, robustness_df_IU_cat.iloc[high_coop_IU_solutions[0]]], axis=0, ignore_index=True)
robustness_base_cat = pd.concat([robustness_df_base_cat, robustness_df_base_cat.iloc[high_coop_base_solutions[0]]], axis=0, ignore_index=True)

# drop the regional column for plotting
robustness_df_base_cat_noReg = robustness_df_base_cat.drop(columns=['Regional'])
robustness_df_IU_cat_noReg = robustness_df_IU_cat.drop(columns=['Regional'])
robustness_base_cat_noReg = robustness_base_cat.drop(columns=['Regional'])
robustness_IU_cat_noReg = robustness_IU_cat.drop(columns=['Regional'])
robustness_IU_highcoop_noReg = robustness_IU_highcoop.drop(columns=['Regional'])
robustness_IU_highcoop_noReg['Category'] = 'IU social planner'
robustness_base_highcoop_noReg = robustness_base_highcoop.drop(columns=['Regional'])
robustness_base_highcoop_noReg['Category'] = 'base'

fig, ax = plt.subplots(2,1,figsize=(10,4), gridspec_kw={'hspace':0.1, 'wspace':0.1})
axis_labels = utilities
figname_IU = f'fig_supporting_6a.pdf'
axis_mins = [0.2, 0.2, 0.2]
axis_maxs = [0.9, 0.9, 0.9]

custom_parallel_coordinates(fig, ax, robustness_IU_cat_noReg, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='top', zorder_by=2,
                                alpha_base=0.5, lw_base=0.75, fontsize=14,
                                minmaxs=['max', 'max', 'max'],
                                color_by_categorical='Category',
                                color_dict_categorical=color_dict_coop,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 
                                
custom_parallel_coordinates(fig, ax, robustness_base_cat_noReg, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='top', 
                                alpha_base=0.5, lw_base=0.75, fontsize=14,
                                minmaxs=['max', 'max', 'max'],
                                color_by_categorical='Category',
                                color_dict_categorical=color_dict_coop,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

custom_parallel_coordinates(fig, ax, robustness_IU_highcoop_noReg, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='top', zorder_by=2,
                                alpha_base=1.0, lw_base=4, fontsize=14,
                                minmaxs=['max', 'max', 'max'],
                                color_by_categorical='Category',
                                color_dict_categorical=color_dict_coop,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

custom_parallel_coordinates(fig, ax, robustness_base_highcoop_noReg, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='top', zorder_by=2,
                                alpha_base=1.0, lw_base=4, fontsize=14,
                                minmaxs=['max', 'max', 'max'],
                                color_by_categorical='Category',
                                color_dict_categorical=color_dict_coop,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

plt.title(f'Robustness of selected high coop IU and base solutions under {sim_mode} conditions', fontsize=16)
plt.savefig(f'figures/{figname_IU}.pdf', bbox_inches='tight', dpi=300)
plt.show()