import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_robustness import *

# user can modify these values to select which solutions to plot 
# and where to store the output figure
sp_base_sol = 29
sp_IU_sol = 401
output_figure_filepath = f'figures/robustness_3Dscatter_base_IU_p90.pdf'

# set up plotting parameters
num_sol_dict = {'base': 46, 'IU': 628}
color_dict_coop = {'other': "#E6E6E6", 'base': "#39563D",
                    'IU Social Planner': "#B66D0D"}

utilities = ['Watertown', 'Dryville', 'Fallsland']
util_abbrevs = ['W', 'D', 'F']
obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
objs_allutils = [obj_name + f'_{util_abbrev}' for util_abbrev in util_abbrevs for obj_name in obj_names]
objs_regional = [obj_name + '_R' for obj_name in obj_names]

# read in the robustness dataframes from csv
robustness_df_IU = pd.read_csv(f'../../results/DU Reevaluation/robustness_sim_p90_refset_IU.csv')
robustness_df_base = pd.read_csv(f'../../results/DU Reevaluation/robustness_sim_p90_refset_base.csv')

# plot 3D scatter highlighting the three highlighted solutions
fig, ax3d = plt.subplots(1,1,figsize=(8,8), subplot_kw={'projection': '3d'})

ax3d.scatter(robustness_df_base['Dryville'], robustness_df_base['Fallsland'], robustness_df_base['Watertown'], 
             color="#D4D3D3", s=100, alpha=0.5, label='All solutions')
ax3d.scatter(robustness_df_IU['Dryville'], robustness_df_IU['Fallsland'], robustness_df_IU['Watertown'], 
             color="#D4D3D3", s=100, alpha=0.5, label='All solutions')
ax3d.scatter(robustness_df_base.loc[sp_base_sol, 'Dryville'], robustness_df_base.loc[sp_base_sol, 'Fallsland'], robustness_df_base.loc[sp_base_sol, 'Watertown'],
             color=color_dict_coop['base'], s=170, label='Baseline')
ax3d.scatter(robustness_df_IU.loc[sp_IU_sol, 'Dryville'], robustness_df_IU.loc[sp_IU_sol, 'Fallsland'], robustness_df_IU.loc[sp_IU_sol, 'Watertown'],
             color=color_dict_coop['IU social planner'], s=170, label='IU social planner')

ax3d.set_xlabel('Dryville robustness', fontsize=12)
ax3d.set_ylabel('Fallsland robustness', fontsize=12)
ax3d.set_zlabel('Watertown robustness', fontsize=12)

ax3d.set_title(f'3D scatter of robustness for all\nsolutions under WC10 conditions', fontsize=16)
ax3d.legend(fontsize=10, loc='lower center', bbox_to_anchor=(0.5, -0.20), ncol=3, frameon=False)
plt.savefig(output_figure_filepath, bbox_inches='tight', dpi=300)