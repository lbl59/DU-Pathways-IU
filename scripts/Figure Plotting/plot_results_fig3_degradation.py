import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_iu import *
from quantify_perturbations import *

# import Line2D and Patch for legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# setup attributes to be set by user
sim_mode = 'p90'

obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
util_abbrevs = ['W', 'D', 'F']

# append obj names to util_abbrevs
objs_utils = [f'{obj}_{util}' for util in util_abbrevs for obj in obj_names]
objs_regional =  [f'{obj}_R' for obj in obj_names]
objs_W = [f'{obj}_W' for obj in obj_names]
objs_D = [f'{obj}_D' for obj in obj_names]
objs_F = [f'{obj}_F' for obj in obj_names]
objs_all = objs_utils + objs_regional

# import IU performance objectives 
objs_original_df_IU = pd.read_csv(f'../../results/DU Optimization/objectives_IU_{sim_mode}_nd.csv', index_col=None, header=None)
objs_original_df_IU.columns = objs_utils
objs_original_regional_df_IU = pd.read_csv(f'../../results/DU Optimization/objectives_IU_{sim_mode}_regional.csv', index_col=None, header=None)
objs_original_w_regional_df_IU = pd.concat([objs_original_df_IU, objs_original_regional_df_IU], axis=1)

# import baseline performance objectives
objs_original_df_base = pd.read_csv(f'../../results/DU Optimization/objectives_base_{sim_mode}_nd.csv', index_col=None, header=None)
objs_original_df_base.columns = objs_utils
objs_original_regional_df_base = pd.read_csv(f'../../results/DU Optimization/objectives_base_{sim_mode}_regional.csv', index_col=None, header=None)
objs_original_w_regional_df_base = pd.concat([objs_original_df_base, objs_original_regional_df_base], axis=1)

# plot a 2x4 grid of histograms, with the x-axis being the bins and the y-axis being the count of solutions in each bin
fig, axs = plt.subplots(4, 2, figsize=(9, 9), sharex=True, sharey=False, gridspec_kw={'hspace': 0.3, 'wspace': 0.2})
