import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_iu import *

from helper_quantify_perturbations import *

# import Line2D and Patch for legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# setup attributes to be set by user
sim_mode = 'p90'
output_figures_filename_hist = 'figures/freq_degradation_histograms_pct.pdf'
output_figures_filename_heatmap = 'figures/robustness_degradation_histograms.pdf'

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

# bin each of the max_percent_degradation arrays into 20 bins and count the number of solutions in each bin
num_bins = 10
bins = np.linspace(0, 1.0, num_bins)  # 10 bins from 0 to 1.0
# Then you create histograms with bins=20
hist_degradation_IU_W, _ = np.histogram(max_percent_degradation_IU_W, bins=num_bins)
hist_degradation_IU_D, _ = np.histogram(max_percent_degradation_IU_D, bins=num_bins)
hist_degradation_IU_F, _ = np.histogram(max_percent_degradation_IU_F, bins=num_bins)

hist_degradation_base_W, _ = np.histogram(max_percent_degradation_base_W, bins=num_bins)
hist_degradation_base_D, _ = np.histogram(max_percent_degradation_base_D, bins=num_bins)
hist_degradation_base_F, _ = np.histogram(max_percent_degradation_base_F, bins=num_bins)

# calculate percent of solutions in each bin 
hist_degradation_W_base_percent = hist_degradation_base_W / np.sum(hist_degradation_base_W) * 100
hist_degradation_D_base_percent = hist_degradation_base_D / np.sum(hist_degradation_base_D) * 100
hist_degradation_F_base_percent = hist_degradation_base_F / np.sum(hist_degradation_base_F) * 100

hist_degradation_W_IU_percent = hist_degradation_IU_W / np.sum(hist_degradation_IU_W) * 100
hist_degradation_D_IU_percent = hist_degradation_IU_D / np.sum(hist_degradation_IU_D) * 100
hist_degradation_F_IU_percent = hist_degradation_IU_F / np.sum(hist_degradation_IU_F) * 100

hist_degradation_IU, _ = np.histogram(max_percent_degradation_IU_allobjs, bins=num_bins)
hist_degradation_base, _ = np.histogram(max_percent_degradation_base_allobjs, bins=num_bins)

hist_degradation_IU_percent = hist_degradation_IU / np.sum(hist_degradation_IU) * 100
hist_degradation_base_percent = hist_degradation_base / np.sum(hist_degradation_base) * 100

# plot a 2x4 grid of histograms, with the x-axis being the bins and the y-axis being the count of solutions in each bin
fig_hist, axs_hist = plt.subplots(4, 2, figsize=(9, 9), sharex=True, sharey=False, gridspec_kw={'hspace': 0.3, 'wspace': 0.2})

for i, util in enumerate(['Watertown', 'Dryville', 'Fallsland']):
    ax = axs_hist[i, 0]
    ax.hist(bins, bins=bins, weights=hist_degradation_W_base_percent if util == 'Watertown' else hist_degradation_D_base_percent if util == 'Dryville' \
           else hist_degradation_F_base_percent, color='#3E8D8F', alpha=1.0)

    if i == 2:
        ax.set_xlim(0, 1.0)
        ax.set_xticks(np.arange(0, 1.01, 0.05))
        ax.set_xticklabels(np.arange(0, 101, 5).astype(int))
    ax.set_ylabel(f'{util}\n% total strategies')
    ax.set_ylim(0, 40)

    # remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
   
for i, util in enumerate(['Watertown', 'Dryville', 'Fallsland']):
    ax = axs_hist[i, 1]
    ax.hist(bins, bins=bins, weights=hist_degradation_W_IU_percent if util == 'Watertown' else hist_degradation_D_IU_percent if util == 'Dryville' \
           else hist_degradation_F_IU_percent, color='#FBB13C', alpha=1.0)

    if i == 2:
        ax.set_xlim(0, 1.0)
        ax.set_xticks(np.arange(0, 1.01, 0.05))
        ax.set_xticklabels(np.arange(0, 101, 5).astype(int))
    ax.set_ylabel('% total strategies')
    ax.set_ylim(0, 40)

    # remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

axs_hist[3,0].hist(bins, bins=bins, weights=hist_degradation_base_percent, color='#3E8D8F', alpha=1.0)
axs_hist[3,1].hist(bins, bins=bins, weights=hist_degradation_IU_percent, color='#FBB13C', alpha=1.0)

axs_hist[3,0].set_xlabel(r'$\longleftarrow$ Max Percent Degradation')
axs_hist[3,0].set_xlim(0, 1.0)
axs_hist[3,0].set_xticks(np.arange(0, 1.01, 0.1))
axs_hist[3,0].set_xticklabels(np.arange(0, 101, 10).astype(int))
axs_hist[3,1].set_xticks(np.arange(0, 1.01, 0.1))
axs_hist[3,1].set_xticklabels(np.arange(0, 101, 10).astype(int))

axs_hist[3,0].set_ylabel('Regional\n %total strategies')
axs_hist[3,0].set_ylim(0, 40)

# remove top and right spines
axs_hist[3,0].spines['top'].set_visible(False)
axs_hist[3,0].spines['right'].set_visible(False)
axs_hist[3,1].spines['top'].set_visible(False)
axs_hist[3,1].spines['right'].set_visible(False)

# add a legend 
custom_lines = [Patch(facecolor='#3E8D8F', edgecolor='black', label='IU'),
                Patch(facecolor='#FBB13C', edgecolor='black', label='Base')]
legend = fig_hist.legend(handles=custom_lines, loc='lower center', ncol=2, fontsize=14, frameon=False, bbox_to_anchor=(0.5, 0.0))
plt.savefig(output_figures_filename_hist, dpi=300, bbox_inches='tight')


# plot single-line heatmaps for each utility, with the x-axis being the bins and the y-axis being the count of solutions in each bin
fig_hm, axs_hm = plt.subplots(4, 2, figsize=(9, 3), sharex=True, sharey=False, gridspec_kw={'hspace': 0.3, 'wspace': 0.2})

for i, util in enumerate(['Watertown', 'Dryville', 'Fallsland']):
    ax = axs_hm[i, 0]
    # turn on borders for each subplot
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    hmap_vals = hist_degradation_base_W if util == 'Watertown' else hist_degradation_base_D if util == 'Dryville' else hist_degradation_base_F
    # plot heatmap where color is number of solutions in each bin
    sns.heatmap(hmap_vals.reshape(1,-1), ax=ax, cbar=False, cmap='Greens', xticklabels=np.arange(0, 101, 10).astype(int), yticklabels=[],
                vmin=0, vmax=25)

for i, util in enumerate(['Watertown', 'Dryville', 'Fallsland']):
    ax = axs_hm[i, 1]
    hmap_vals = hist_degradation_IU_W if util == 'Watertown' else hist_degradation_IU_D if util == 'Dryville' else hist_degradation_IU_F
    sns.heatmap(hmap_vals.reshape(1, -1), ax=ax, cbar=False, cmap='Oranges', xticklabels=np.arange(0, 101, 10).astype(int), yticklabels=[],
                vmin=0, vmax=250)

sns.heatmap(hist_degradation_base.reshape(1, -1), ax=axs_hm[3,0], cbar=False, cmap='Greens', xticklabels=np.arange(0, 101, 10).astype(int), yticklabels=[],
            vmin=0, vmax=25)
sns.heatmap(hist_degradation_IU.reshape(1, -1), ax=axs_hm[3,1], cbar=False, cmap='Oranges', xticklabels=np.arange(0, 101, 10).astype(int), yticklabels=[],
            vmin=0, vmax=250)

# add a colorbar to the bottom of each column 
cbar_base = fig_hm.colorbar(axs_hm[3,0].collections[0], ax=axs_hm[:,0], orientation='horizontal', fraction=0.05, pad=0.15)
cbar_base.set_label(r'Number of strategies $\longrightarrow$', fontsize=12)
cbar_IU = fig_hm.colorbar(axs_hm[3,1].collections[0], ax=axs_hm[:,1], orientation='horizontal', fraction=0.05, pad=0.15)
cbar_IU.set_label(r'Number of strategies $\longrightarrow$', fontsize=12)

plt.savefig(output_figures_filename_heatmap, dpi=300, bbox_inches='tight')