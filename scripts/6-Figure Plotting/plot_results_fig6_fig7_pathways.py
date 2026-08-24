import numpy as np
import os
import matplotlib.pyplot as plt
from helper_plot_pathways_functions import *

# Find original pathways in this Hopper folder: /home/fs02/pmr82_0001/lbl59/OptimalAction/code/DUOpt_output/fulloutput_ptb_IU/pathways/

refset_mode = 'IU'
dv_mode = refset_mode
sol_num = 401

sim_mode_colors_coop = {'base': "#39563D",
                        'IU_pw': "#FBB13C", 'IU_sp': "#B66D0D"}

sols_dict = {401: 'IU_sp', 29: 'base'}
sol_selected = sols_dict[sol_num]

# dict that maps perturebed instance with the maximum percent degradation for the solution of interest
max_ptb_instance_dict = {401: 316, 29: 253}
max_ptb_instance = max_ptb_instance_dict[sol_num]

sols_color_list = {'IU_sp': ["#BEA482", '#B66D0D', "#7B4A09"],
                   'base': ["#A6BEA9", "#507054", "#0D4213"]}

path_color = sols_color_list[sol_selected]

watertown_inf = ['Baseline', 'New River\nReservoir',
                     'College Rock\nExpansion Low',
                     'College Rock\nExpansion High', 'Water Reuse',
                     'Water Reuse II']
dryville_inf = ['', 'Baseline', '', 'Sugar Creek\nReservoir', '', 'Water Reuse']
fallsland_inf = ['', 'Baseline', '', 'New River\nReservoir', '', 'Water Reuse']

infra_dict = {'watertown': watertown_inf,
              'dryville': dryville_inf,
              'fallsland': fallsland_inf}

num_reals = 200

# cluster_pathways(filepath, solution, utility, num_reals, num_clusters)
pathway_dir = f'perturbed_pathways_{dv_mode}'
fig_dir = f'figures'

# make a directory for the figures if it doesn't exist
if not os.path.exists(fig_dir):
    os.makedirs(fig_dir)

heavy_inf_color = path_color[2]
mid_inf_color = path_color[1]
light_inf_color = path_color[0]

print(f'Clustering pathways for solution {sol_num}...')
watertown_num_clusters, watertown_cluster_pathways, watertown_cluster_meds = \
    cluster_pathways(pathway_dir, f"{sol_num}_original", 'watertown', num_reals)
dryville_num_clusters, dryville_cluster_pathways, dryville_cluster_meds = \
    cluster_pathways(pathway_dir, f"{sol_num}_original", 'dryville', num_reals)
fallsland_num_clusters, fallsland_cluster_pathways, fallsland_cluster_meds = \
    cluster_pathways(pathway_dir, f"{sol_num}_original", 'fallsland', num_reals)

print(f"Watertown clusters: {watertown_num_clusters}")
print(f"Dryville clusters: {dryville_num_clusters}")
print(f"Fallsland clusters: {fallsland_num_clusters}")

print(f'Plotting pathways for solution {sol_num} under {dv_mode} conditions...')

title_label = f'Solution {sol_num}\n{dv_mode} ref. set simulated under {dv_mode} conditions'
fig_name = f'{fig_dir}/pathways_{dv_mode}_sol{sol_num}_withlegend_newver.pdf'    

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True, 
                                   figsize=(2.5,8), dpi=300,
                                   gridspec_kw={'height_ratios': [1,1,1]})

# remove x-tick labels for all but bottom plot
ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

ax1.set_ylabel('Watertown', fontsize=12)
ax1.set_yticks(np.arange(0, 6))
ax1.set_yticklabels(watertown_inf, fontsize=10)

ax2.set_ylabel('Dryville', fontsize=12)
ax2.set_yticks(np.linspace(-0.65, 2.15, 6))
ax2.set_yticklabels(dryville_inf, fontsize=10)

ax3.set_xlabel('Years in simulation', fontsize=14)
ax3.set_ylabel('Fallsland', fontsize=12)
ax3.set_yticks(np.linspace(-0.65, 2.15, 6))
ax3.set_yticklabels(fallsland_inf, fontsize=10)

if watertown_num_clusters != None:
    print('Creating Watertown cluster plots...')
    
    create_cluster_plots_single(watertown_cluster_meds, watertown_cluster_pathways,
                            watertown_num_clusters, infra_dict['watertown'],
                            [light_inf_color, mid_inf_color, heavy_inf_color],
                            ['bone_r', 'bone_r', 'bone_r'], ax1)


if dryville_num_clusters != None:
    
    create_cluster_plots_single(dryville_cluster_meds, dryville_cluster_pathways,
                            dryville_num_clusters, infra_dict['dryville'],
                            [light_inf_color, mid_inf_color, heavy_inf_color],
                            ['bone_r', 'bone_r', 'bone_r'], ax2)


if fallsland_num_clusters != None:
    
    create_cluster_plots_single(fallsland_cluster_meds, fallsland_cluster_pathways,
                            fallsland_num_clusters, infra_dict['fallsland'],
                            [light_inf_color, mid_inf_color, heavy_inf_color],
                            ['bone_r', 'bone_r', 'bone_r'], ax3, plot_cbar=False)

ax1.tick_params(axis = "y", which = "both", left = False, right = False)

ax2.tick_params(axis = "y", which = "both", left = False, right = False)

ax3.tick_params(axis = "y", which = "both", left = False, right = False)

# insert a legend for the vertical bar plots
# set x-axis limits
ax1.set_xlim([0, 45])
ax2.set_xlim([0, 45])
ax3.set_xlim([0, 45])

plt.suptitle(title_label, fontsize=16, y=1.00)
plt.savefig(fig_name)
plt.show()

