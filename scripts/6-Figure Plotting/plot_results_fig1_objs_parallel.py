import pandas as pd 
import numpy as np 

import seaborn as sns
from helper_functions_objs import *

import matplotlib.pyplot as plt 
from matplotlib import colormaps, cm
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from pandas.plotting import parallel_coordinates

from ..parallel_plot_functions import *

obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
util_abbrevs = ['W', 'D', 'F']

# append obj names to util_abbrevs
objs_utils = [f'{obj}_{util}' for util in util_abbrevs for obj in obj_names]
objs_regional =  [f'{obj}_R' for obj in obj_names]
objs_W = [f'{obj}_W' for obj in obj_names]
objs_D = [f'{obj}_D' for obj in obj_names]
objs_F = [f'{obj}_F' for obj in obj_names]

color_dict_coop = {'Base': "#588157", 'IU': "#F5A36D"}

# change depending on whether the Expected or WC10 formulation is being used
obj_mode = 'avg'  # avg or p10
actions_mode = 'base'

if obj_mode == 'p10':
    action_mode = 'IU'

# change depending on where user would like to save the output
output_filename = f'figures/parallel_refset_{obj_mode}_{actions_mode}_regional.pdf'

# read in objectives
objs_truncated_allutils = pd.read_csv(f'../results/DU Optimization/objectives_dvs_nd/objectives_{actions_mode}_{obj_mode}_nd.csv', index_col=False, header=None)
objs_truncated_allutils.columns = objs_utils


# split objectives by utility
objs_W = objs_truncated_allutils[[f'{obj}_W' for obj in obj_names]]
objs_D = objs_truncated_allutils[[f'{obj}_D' for obj in obj_names]]
objs_F = objs_truncated_allutils[[f'{obj}_F' for obj in obj_names]]

# find regional minimax solutions
objs_reg = find_regional_minimax(objs_truncated_allutils, obj_names)

objs_reg_cat = objs_reg.copy()
utility_parallel = "Regional"

if actions_mode == 'base':
    objs_reg_cat['Category'] = f"Base"
elif actions_mode == 'IU':
    objs_reg_cat['Category'] = f"IU"


# setup figure specifications and dimensions
figsize = (9,4)
fontsize = 14

# cap axis mins and maxs to reasonable values
axis_mins = [0.97, 0.0, 0.0,0.0,0.0]
axis_maxs = [1.0, 0.3, 100.0, 0.2, 0.2]
# get the axis labels 
axis_labels = objs_reg_cat.columns.tolist()[:-1]

### create figure
fig, ax = plt.subplots(1,1,figsize=figsize, gridspec_kw={'hspace':0.1, 'wspace':0.1})
custom_parallel_coordinates(fig, ax, objs_reg_cat, columns_axes=axis_labels, 
                                axis_labels=axis_labels, 
                                ideal_direction='bottom',
                                alpha_base=0.7, lw_base=1.1, fontsize=fontsize,
                                minmaxs=['max','min','min','min','min'], 
                                colorbar_ticks_continuous=range(0,1,5),
                                color_by_categorical = 'Category', 
                                color_dict_categorical=color_dict_coop,
                                axis_mins=axis_mins, axis_maxs=axis_maxs) 

ax.set_title(f'Tradeoffs for {utility_parallel}\n(risk-averse formulation)', fontsize=fontsize+2, pad=20)
plt.savefig(output_filename, dpi=300, bbox_inches='tight')