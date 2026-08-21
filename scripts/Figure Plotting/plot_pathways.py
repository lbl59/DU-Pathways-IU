#%%
import numpy as np
import os
import matplotlib.pyplot as plt
from plot_pathways_functions import cluster_pathways, \
    cluster_pathways_perturbed, \
    create_cluster_plots_single, \
    overlay_violin_timing_frequency


# Find original pathways in this Hopper folder: /home/fs02/pmr82_0001/lbl59/OptimalAction/code/DUOpt_output/fulloutput_ptb_IU/pathways/

refset_mode = 'IU'
dv_mode = refset_mode
sol_num = 363

sim_mode_colors_coop = {'base': "#39563D",
                        'IU_pw': "#FBB13C", 'IU_sp': "#B66D0D"}

sols_dict = {401: 'IU_sp', 363: 'IU_pw', 29: 'base'}
sol_selected = sols_dict[sol_num]

#%%
sols_color_list = {'IU_sp': ["#BEA482", '#B66D0D', "#7B4A09"],
                   'IU_pw': ["#F3E6D1", '#FBB13C', "#B06F05"],
                   'base': ["#87A18A", '#39563D', "#0D4213"]}

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

num_ptb = 500
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

#%%

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

#%%
'''
print(f'Clustering perturbed pathways for solution {sol_num}...')
watertown_cluster_pathways_ptb, watertown_cluster_medians_ptb = cluster_pathways_perturbed(f"{pathway_dir}/pathways_ptb_s{sol_num}", 
                                                                                            num_ptb, num_reals, 'watertown',
                                                                                            watertown_num_clusters)
dryville_cluster_pathways_ptb, dryville_cluster_medians_ptb = cluster_pathways_perturbed(f"{pathway_dir}/pathways_ptb_s{sol_num}", 
                                                                                            num_ptb, num_reals, 'dryville',
                                                                                            dryville_num_clusters)

fallsland_cluster_pathways_ptb, fallsland_cluster_medians_ptb = cluster_pathways_perturbed(f"{pathway_dir}/pathways_ptb_s{sol_num}", 
                                                                                            num_ptb, num_reals, 'fallsland',
                                                                                            fallsland_num_clusters)
'''
#%%
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
    '''
    w_cols = list(range(watertown_cluster_meds.shape[1]))         # 5 cols
    w_ypos = np.arange(1, len(w_cols) + 1)                        # 1..5
    infra_to_ypos_w = dict(zip(w_cols, w_ypos))
    print('Overlaying violin plots for Watertown...')
    overlay_violin_timing_frequency(watertown_cluster_medians_ptb,
                            infra_to_ypos_w, 
                            [light_inf_color, mid_inf_color, heavy_inf_color], ax1)
    '''

if dryville_num_clusters != None:
    
    create_cluster_plots_single(dryville_cluster_meds, dryville_cluster_pathways,
                            dryville_num_clusters, infra_dict['dryville'],
                            [light_inf_color, mid_inf_color, heavy_inf_color],
                            ['bone_r', 'bone_r', 'bone_r'], ax2)
    '''
    d_cols = list(range(dryville_cluster_meds.shape[1]))          # likely 2 cols
    d_ypos = np.arange(1, len(d_cols) + 1)                        # 1..2
    infra_to_ypos_d = dict(zip(d_cols, d_ypos))
    print('Overlaying violin plots for Dryville...')
    overlay_violin_timing_frequency(dryville_cluster_medians_ptb,
                            infra_to_ypos_d, 
                            [light_inf_color, mid_inf_color, heavy_inf_color], ax2)
    '''

if fallsland_num_clusters != None:
    
    create_cluster_plots_single(fallsland_cluster_meds, fallsland_cluster_pathways,
                            fallsland_num_clusters, infra_dict['fallsland'],
                            [light_inf_color, mid_inf_color, heavy_inf_color],
                            ['bone_r', 'bone_r', 'bone_r'], ax3, plot_cbar=False)
    '''
    f_cols = list(range(fallsland_cluster_meds.shape[1]))         # likely 2 cols
    f_ypos = np.arange(1, len(f_cols) + 1)                        # 1..2
    infra_to_ypos_f = dict(zip(f_cols, f_ypos))  
    print('Overlaying violin plots for Fallsland...')   
    overlay_violin_timing_frequency(fallsland_cluster_medians_ptb,
                            infra_to_ypos_f, 
                            [light_inf_color, mid_inf_color, heavy_inf_color], ax3)
    '''
ax1.tick_params(axis = "y", which = "both", left = False, right = False)

ax2.tick_params(axis = "y", which = "both", left = False, right = False)

ax3.tick_params(axis = "y", which = "both", left = False, right = False)
'''
ax3.legend(['Light inf.', 'Moderate inf.', 'Heavy inf.'],
        loc='lower left')
'''

'''
# add a bone_r colorbar to the right of the subplots
cbar_ax = fig.add_axes([0.1, 0.05, 1.0, 0.05])  # [left, bottom, width, height]
cbar_ax.axis('off')  # hide the axes
# get the colors from the bone_r colormap
cmap = plt.get_cmap('bone_r')
colors = [cmap(i) for i in np.linspace(0, 50, 100)]  # 100 colors from the colormap
# create a colorbar using the colors
cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), cax=cbar_ax, orientation='horizontal')
cbar.set_ticks([0, 0.5, 1])
cbar.set_ticklabels(['0%', '25%', '50%'])
cbar.set_label('Frequency of pathway occurrence\nin perturbed runs', fontsize=10)
'''
# insert a legend for the vertical bar plots
# set x-axis limits
ax1.set_xlim([0, 45])
ax2.set_xlim([0, 45])
ax3.set_xlim([0, 45])

plt.suptitle(title_label, fontsize=16, y=1.00)
#plt.tight_layout()
plt.savefig(fig_name)
plt.show()

# %%
