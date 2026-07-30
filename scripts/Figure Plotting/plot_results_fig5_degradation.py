import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_iu import *

from ..quantify_perturbations import *

# import Line2D and Patch for legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# user defined parameters for which solutions to plot and where to save the output figure
sp_base_sol = 29
sp_IU_sol = 401
output_figure_filepath = f'figures/perturbations_allsols_3dscatter_p90.pdf'

obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
util_abbrevs = ['W', 'D', 'F']

# append obj names to util_abbrevs
objs_utils = [f'{obj}_{util}' for util in util_abbrevs for obj in obj_names]
objs_regional =  [f'{obj}_R' for obj in obj_names]
objs_W = [f'{obj}_W' for obj in obj_names]
objs_D = [f'{obj}_D' for obj in obj_names]
objs_F = [f'{obj}_F' for obj in obj_names]
objs_all = objs_utils + objs_regional

# import the degradation statistics for IU and baseline solutions
freq_df_IU = pd.read_csv(f'../../results/IU Reevaluation/perturbations_IU/freq_degradation_allsols_IU_p90.csv', index_col=None, header=0)
max_percent_degradation_df_IU = pd.read_csv(f'../../results/IU Reevaluation/perturbations_IU/percent_degradation_max_allsols_IU_{sim_mode}.csv', index_col=None, header=0)
objs_all_sat = [obj for obj in objs_all if ('INPC' not in obj and 'PFC' not in obj)]
max_percent_degradation_IU_allobjs = max_percent_degradation_df_IU[objs_all_sat].max(axis=1).values

freq_df_base = pd.read_csv(f'../../results/IU Reevaluation/perturbations_base/freq_degradation_allsols_base_p90.csv', index_col=None, header=0)
max_percent_degradation_df_base = pd.read_csv(f'../../results/IU Reevaluation/perturbations_base/percent_degradation_max_allsols_base_{sim_mode}.csv', index_col=None, header=0)
max_percent_degradation_base_allobjs = max_percent_degradation_df_base[objs_all_sat].max(axis=1).values

objs_all_sat_W = [obj for obj in objs_all_sat if '_W' in obj]
objs_all_sat_D = [obj for obj in objs_all_sat if '_D' in obj]
objs_all_sat_F = [obj for obj in objs_all_sat if '_F' in obj]

max_percent_degradation_IU_W = max_percent_degradation_df_IU[objs_all_sat_W].max(axis=1).values
max_percent_degradation_IU_D = max_percent_degradation_df_IU[objs_all_sat_D].max(axis=1).values
max_percent_degradation_IU_F = max_percent_degradation_df_IU[objs_all_sat_F].max(axis=1).values

max_percent_degradation_base_W = max_percent_degradation_df_base[objs_all_sat_W].max(axis=1).values
max_percent_degradation_base_D = max_percent_degradation_df_base[objs_all_sat_D].max(axis=1).values
max_percent_degradation_base_F = max_percent_degradation_df_base[objs_all_sat_F].max(axis=1).values

# 3d scatter plot of max percent degradation for W, D, F for IU and base
color_dict_coop = {'other': "#D4D3D3", 'base': "#39563D", 'IU social planner': "#B66D0D"}

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(max_percent_degradation_IU_W, max_percent_degradation_IU_D, max_percent_degradation_IU_F, 
           color=color_dict_coop['other'], alpha=0.5, label='All solutions', s=100)
ax.scatter(max_percent_degradation_base_D[sp_base_sol], max_percent_degradation_base_F[sp_base_sol], \
    max_percent_degradation_base_W[sp_base_sol], 
           color=color_dict_coop['base'], alpha=1.0, label='Baseline', s=170)
ax.scatter(max_percent_degradation_IU_D[sp_IU_sol], max_percent_degradation_IU_F[sp_IU_sol], \
    max_percent_degradation_IU_W[sp_IU_sol], 
           color=color_dict_coop['IU social planner'], alpha=1.0, label='IU Social Planner', s=170)

# inverse the axes so that higher degradation is closer to the origin
ax.set_xlim(ax.get_xlim()[::-1])
ax.set_ylim(ax.get_ylim()[::-1])
ax.set_zlim(ax.get_zlim()[::-1])

ax.set_xlabel(r'$\longleftarrow$' + 'Dryville max performance\ndegradation (%)', fontsize=12, labelpad=10)
ax.set_ylabel(r'$\longleftarrow$' + 'Fallsland max performance\ndegradation (%)', fontsize=12, labelpad=10)
ax.set_zlabel(r'$\longleftarrow$' + 'Watertown max performance\ndegradation (%)', fontsize=12, labelpad=10)

ax.set_title(f'3D scatter of worst-case performance degradation for all\nsolutions under WC10 conditions', fontsize=16)
ax.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, -0.20), ncol=3, frameon=False)
plt.tight_layout()
plt.savefig(output_figure_filepath, bbox_inches='tight', dpi=300)