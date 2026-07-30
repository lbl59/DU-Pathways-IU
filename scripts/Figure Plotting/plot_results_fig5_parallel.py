import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from ..helper_functions_objs import *

from matplotlib import colormaps, cm
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from pandas.plotting import parallel_coordinates
from parallel_plot_functions import *

# solutions of interest and the utility of whose parallel coordinates will be plotted. 
# These values can be modified by the user 
social_planner_IU = 401
social_planner_base = 29
util_selected = 'W'
output_figure_filepath = f'figures/parallel_objs_IUbase_{util_selected}_p90.pdf'

obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
util_abbrevs = ['W', 'D', 'F']

# append obj names to util_abbrevs
objs_utils = [f'{obj}_{util}' for util in util_abbrevs for obj in obj_names]
objs_regional =  [f'{obj}_R' for obj in obj_names]
objs_W = [f'{obj}_W' for obj in obj_names]
objs_D = [f'{obj}_D' for obj in obj_names]
objs_F = [f'{obj}_F' for obj in obj_names]
util_dict = {'W':'Watertown', 'D':'Dryville', 'F':'Fallsland'}

# read in objectives
objs_truncated_base_allutils = pd.read_csv(f'../../results/DU Optimization/objectives_dvs_nd/objectives_base_p90_nd.csv', index_col=False, header=None)
objs_truncated_base_allutils.columns = objs_utils
objs_truncated_IU_allutils = pd.read_csv(f'../../results/DU Optimization/objectives_IU_p90_nd.csv', index_col=False, header=None)
objs_truncated_IU_allutils.columns = objs_utils

# split objectives by utility
objs_W_IU = objs_truncated_IU_allutils[[f'{obj}_W' for obj in obj_names]]
objs_D_IU = objs_truncated_IU_allutils[[f'{obj}_D' for obj in obj_names]]
objs_F_IU = objs_truncated_IU_allutils[[f'{obj}_F' for obj in obj_names]]

objs_W_base = objs_truncated_base_allutils[[f'{obj}_W' for obj in obj_names]]
objs_D_base = objs_truncated_base_allutils[[f'{obj}_D' for obj in obj_names]]
objs_F_base = objs_truncated_base_allutils[[f'{obj}_F' for obj in obj_names]]

# find regional minimax solutions
objs_reg_base = find_regional_minimax(objs_truncated_base_allutils, obj_names)
objs_reg_IU = find_regional_minimax(objs_truncated_IU_allutils, obj_names)

# combine regional with main set of objectives 
objs_IU_all = pd.concat([objs_truncated_IU_allutils, objs_reg_IU], axis=1)
objs_base_all = pd.concat([objs_truncated_base_allutils, objs_reg_base], axis=1)

sim_mode_colors_coop = {'base': "#39563D", 'social planner': "#B66D0D"}

sols_to_highlight = {"baseline": [social_planner_base], "social planner": [social_planner_IU]}

sim_mode_colors_IU = {'others': 'gainsboro', 'social planner': "#B66D0D"}
sim_mode_colors_base = {'others': 'gainsboro', 'baseline': "#39563D"}

# high_coop_sols 
social_planner_IU_df = pd.DataFrame(objs_IU_all.loc[[social_planner_IU]].values, columns=objs_IU_all.columns)
baseline_df = pd.DataFrame(objs_base_all.loc[[social_planner_base]].values, columns=objs_base_all.columns)

# categorized objectives 
objs_IU_all_cat = objs_IU_all.copy()
objs_IU_all_cat['Category'] = 'others'
social_planner_IU_df['Category'] = 'social planner'
objs_IU_all_cat = pd.concat([objs_IU_all_cat, social_planner_IU_df], axis=0, ignore_index=True)

objs_base_all_cat = objs_base_all.copy()
objs_base_all_cat['Category'] = 'others'
baseline_df['Category'] = 'baseline'
objs_base_all_cat = pd.concat([objs_base_all_cat, baseline_df], axis=0, ignore_index=True)

util_selected = 'W'
cols_to_plot = [f'REL_{util_selected}', f'RF_{util_selected}', f'INPC_{util_selected}', f'PFC_{util_selected}', f'WCC_{util_selected}'] + ['Category']

objs_IU_to_plot = objs_IU_all_cat[cols_to_plot]
objs_base_to_plot = objs_base_all_cat[cols_to_plot]

# setup figure specifications and dimensions
figsize = (9,4)
fontsize = 14

axis_mins = [0.85, 0.0, 0.0,0.0,0.0]
axis_maxs = [1.0, 0.7, 350.0, 0.5, 0.7]

axis_labels = objs_IU_to_plot.columns.tolist()[:-1]

### create figure
fig, ax = plt.subplots(1,1,figsize=figsize, gridspec_kw={'hspace':0.1, 'wspace':0.1})

# all IU solutions in the background
custom_parallel_coordinates(fig, ax, objs_IU_to_plot, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='bottom',
                                alpha_base=0.5, lw_base=1, fontsize=fontsize,
                                minmaxs=['max','min','min','min','min'], 
                                colorbar_ticks_continuous=range(0,1,5),
                                color_by_categorical = 'Category', 
                                color_dict_categorical=sim_mode_colors_IU,
                                axis_mins=axis_mins, axis_maxs=axis_maxs)

# all baseline solutions in the background
custom_parallel_coordinates(fig, ax, objs_base_to_plot, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='bottom',
                                alpha_base=0.5, lw_base=1, fontsize=fontsize,
                                minmaxs=['max','min','min','min','min'], 
                                colorbar_ticks_continuous=range(0,1,5),
                                color_by_categorical = 'Category', 
                                color_dict_categorical=sim_mode_colors_base,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

custom_parallel_coordinates(fig, ax, baseline_df, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='bottom',
                                alpha_base=1.0, lw_base=3.5, fontsize=fontsize,
                                minmaxs=['max','min','min','min','min'], 
                                colorbar_ticks_continuous=range(0,1,5),
                                color_by_categorical = 'Category', 
                                color_dict_categorical=sim_mode_colors_base,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

# solution 407 from the IU reference set
custom_parallel_coordinates(fig, ax, social_planner_IU_df, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='bottom',
                                alpha_base=1.0, lw_base=3.5, fontsize=fontsize,
                                minmaxs=['max','min','min','min','min'], 
                                colorbar_ticks_continuous=range(0,1,5),
                                color_by_categorical = 'Category', 
                                color_dict_categorical=sim_mode_colors_IU,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

# create a legend 
handles = [Line2D([0], [0], color=sim_mode_colors_IU['social planner'], lw=2, label='IU social planner coop'),
           Line2D([0], [0], color=sim_mode_colors_IU['power index'], lw=2, label='IU power index coop'),
              Line2D([0], [0], color=sim_mode_colors_base['baseline'], lw=2, label='Baseline')]
plt.legend(handles=handles, loc='lower center', fontsize=fontsize-4, frameon=False, bbox_to_anchor=(0.5, 0.0), ncols=5)

plt.savefig(output_figure_filepath, dpi=300, bbox_inches='tight')