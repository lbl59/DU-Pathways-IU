import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_iu import *

action_mode = 'IU'
sol_num = 401
max_ptb_instance_dict = {401: 316, 29: 253}
max_ptb_instance = max_ptb_instance_dict[sol_num]
color_sol_dict = {401: "#B66D0D", 29: "#34563A"}
color_circles_dict = {401: "#FDBF6D", 29: "#ADC7B1"}

objs_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
util_names = ['Watertown', 'Dryville', 'Fallsland', 'Regional']
objs_names_allutils = [obj_name + '_' + util_name[0] for util_name in util_names for obj_name in objs_names]

obj_names_W = ['REL_W', 'RF_W', 'INPC_W', 'PFC_W', 'WCC_W']
obj_names_D = ['REL_D', 'RF_D', 'INPC_D', 'PFC_D', 'WCC_D']
obj_names_F = ['REL_F', 'RF_F', 'INPC_F', 'PFC_F', 'WCC_F']
obj_names_reg = ['REL_R', 'RF_R', 'INPC_R', 'PFC_R', 'WCC_R']
obj_names_dict = {'W': obj_names_W, 'D': obj_names_D, 'F': obj_names_F, 'reg': obj_names_reg}

perturbations_relative_change_filename = f'perturbations_{action_mode}/percent_degradation/sol{sol_num}_sim_p90_weighted.csv'
# get the perturbation 
perturbations_relative_change_df = pd.read_csv(perturbations_relative_change_filename, index_col=None, header=0)
perturbations_relative_change_ptb = perturbations_relative_change_df.iloc[max_ptb_instance_dict[sol_num], :].values

perturbations_relative_change_util_dict = {'Watertown': perturbations_relative_change_df[obj_names_W].iloc[max_ptb_instance_dict[sol_num], :].values,
                                           'Dryville': perturbations_relative_change_df[obj_names_D].iloc[max_ptb_instance_dict[sol_num], :].values,
                                           'Fallsland': perturbations_relative_change_df[obj_names_F].iloc[max_ptb_instance_dict[sol_num], :].values,
                                           'Regional': perturbations_relative_change_df[obj_names_reg].iloc[max_ptb_instance_dict[sol_num], :].values}

# Plot matchstick performance change 
figname = f'figures/percentchange_objs_enoki_sol{sol_num}_ptb{max_ptb_instance}.pdf'
sns.set_style("white")
fig, axes = plt.subplots(4, 1, figsize=(3,12), sharex=True)  # one subplot for each objective
axes = axes.flatten()
plt.subplots_adjust(hspace=0.35)

handles = []
labels = []
x_df = np.arange(0,len(objs_names))
x_rf = np.arange(0,len(objs_names))+0.4

x_pos = [x_df, x_rf]
for i in range(len(util_names)):
    selected_util_df = perturbations_relative_change_util_dict[util_names[i]].copy()

    ymin = selected_util_df.min()
    ymax = selected_util_df.max()
    
    #selected_obj_name = obj_names_full[i]
    axes[i].plot([0, len(objs_names)], [0, 0], color=color_sol_dict[sol_num], linestyle='--', linewidth=2)  # plot horizontal line

    x_vals = x_df
    for x, height in zip(x_vals, selected_util_df):
        axes[i].plot([x, x], [0, height], color=color_sol_dict[sol_num], linewidth=2)  # plot vertical lines
        axes[i].plot(x, height, 'o', color=color_circles_dict[sol_num], markersize=8, 
                        markeredgecolor=color_sol_dict[sol_num], markeredgewidth=2)   # plot points
        
    axes[i].set_ylabel(r'% degradation $\longrightarrow$ ', fontsize=14, fontdict={'fontname': 'Verdana'})
    axes[i].set_ylim(-0.80, 0.81)
    axes[i].set_yticks(np.arange(-0.80, 0.81, 0.20))
    axes[i].set_yticklabels([f'{int(y*100)}' for y in np.arange(-0.80, 0.81, 0.20)], fontsize=11, fontdict={'fontname': 'Verdana'})
    axes[i].set_xticks(np.linspace(0.15,len(objs_names)-0.8, len(objs_names)))
    axes[i].set_xticklabels(objs_names, fontsize=13, fontdict={'fontname': 'Verdana'})
    axes[i].xaxis.set_visible(True)

    # turn off top, bottom, and right spines
    axes[i].spines['top'].set_visible(False)
    axes[i].spines['right'].set_visible(False)
    axes[i].spines['bottom'].set_visible(False)

    # turn on vertical gridlines
    axes[i].xaxis.grid(True)

    axes[i].set_title(util_names[i], fontsize=16, y=1.1, pad = 1, 
                      fontdict={'fontname': 'Verdana'})

handles = [plt.Line2D([], [], color=color_sol_dict[sol_num], marker='o', markersize=12, linestyle='None'),
            plt.Line2D([], [], color=color_sol_dict[sol_num], marker='None', linestyle='--', linewidth=3)]

labels = ['Perturbed instance', 'Original instance']
plt.legend(handles, labels, loc='lower center', ncol=1, bbox_to_anchor=(0.3, -0.6), 
           fontsize=14, frameon=False)

plt.savefig(figname, dpi=300, bbox_inches='tight')
plt.show()