import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from ..helper_functions_robustness import *

# setup attributes to be set by user
sim_mode = 'p90' 
output_figure_filepath = f'figures/robustness_{sim_mode}_conditions.pdf'

# define the number of solutions and figure setup 
num_sol_dict = {'base': 46, 'IU': 628}
yticks_max = {'avg': [0.0, 0.5, 1.0], 'p90': [0.0, 0.45, 0.90]}
sim_mode_colors = {'base': '#6B8F71', 'IU': '#F2B880'}
utilities = ['Watertown', 'Dryville', 'Fallsland']
util_abbrevs = ['W', 'D', 'F']
obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
objs_allutils = [obj_name + f'_{util_abbrev}' for util_abbrev in util_abbrevs for obj_name in obj_names]
objs_regional = [obj_name + '_R' for obj_name in obj_names]

# read in the robustness dataframes from csv
robustness_df_IU = pd.read_csv(f'../../results/DU Reevaluation/robustness_sim_{sim_mode}_refset_IU.csv')
robustness_df_base = pd.read_csv(f'../../results/DU Reevaluation/robustness_sim_{sim_mode}_refset_base.csv')

fig, axs = plt.subplots(3, 1, figsize=(6,7), sharey=True, gridspec_kw={'wspace':0.2, 'hspace':0.5})
utilities = ['Watertown', 'Dryville', 'Fallsland', 'Regional']
plot_robustness_bar(robustness_df_base, robustness_df_IU, 'Watertown', axs[0], sim_mode_colors)
plot_robustness_bar(robustness_df_base, robustness_df_IU, 'Dryville', axs[1], sim_mode_colors)
plot_robustness_bar(robustness_df_base, robustness_df_IU, 'Fallsland', axs[2], sim_mode_colors)

# for each axis, set the y-limit between 0 and 1
for i, ax in enumerate(axs):
    ax.set_yticks(yticks_max[sim_mode])
    ax.set_yticklabels(yticks_max[sim_mode], fontsize=11)
    # draw a horizontal grid line at y=0.5
    ax.axhline(y=0.5, color='k', linestyle='--', linewidth=1.0)
    ax.set_title(f'{utilities[i]}', fontsize=12)
    ax.set_xlabel('Solutions robustness rank', fontsize=10)
    # plot horizontal gridlines
axs[0].set_ylabel('Robustness (%)', fontsize=11)

# set legend at the bottom of the figure without a box
handles, labels = axs[0].get_legend_handles_labels()
labels[0] = 'IU solutions'
labels[1] = 'Base solutions'
plt.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=2, frameon=False, fontsize=10)

plt.suptitle(f'Robustness under {sim_mode} conditions', fontsize=16, y=0.95)
plt.savefig(output_figure_filepath, bbox_inches='tight')
