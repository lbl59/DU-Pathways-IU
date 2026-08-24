import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
 
sns.set_style()
 
# define constants 
NFE = 200000
freq = 2000
num_output = int(NFE/freq)
num_seeds = np.arange(1, 6)  # Assuming 5 seeds
modes = ['base_fullExp', 'IU_fullExp']
seed_colors = ['#FBAF00', '#FFD639', '#FFA3AF', '#007CBE', '#00AF54']
mode_colors = ['coral', 'forestgreen']
mode_names = ['Base', 'Impl. Uncertainty']
#mode_colors = ['forestgreen']
#mode_names = ['Impl. Uncertainty']
problem = 'Sedento'
folder_name = 'output_raw_'
#metric_names = ['Hypervolume', 'GenerationalDistance', 'EpsilonIndicator']
metric_names = ['Hypervolume']
# plot the hypervolume over time
fig, axs = plt.subplots(1, 2, figsize=(9, 5))
# adjust vertical space between subplots
plt.subplots_adjust(hspace=0.1, wspace=0.2)

num_masters = 4
master_ranks = [1, 512, 1023, 1534]
#master_ranks = [1, 50, 99, 148]
num_procs = 2048

for m in range (len(modes)):
    hvol_allseeds_allmasters = np.zeros((num_output, len(num_seeds), len(master_ranks)), dtype=float)
    curr_ax = axs[m]
    curr_ax.set_xlim([freq, NFE+freq])
    for n in range(len(metric_names)):
        metric_name = metric_names[n]
        print(f'Currently processing {modes[m]} with metric {metric_name}')

        # create matrix of hypervolume runtimes 
        hvol_allseeds_min = np.zeros((num_output, len(num_seeds)), dtype=float)
        hvol_allseeds_max = np.zeros((num_output, len(num_seeds)), dtype=float)
        hvol_allseeds = np.zeros((num_output, len(num_seeds)), dtype=float)

        for s in range(len(num_seeds)):
            seed = num_seeds[s]
            hvol_allranks = np.zeros((num_output, len(master_ranks)), dtype=float)    
            
            # read the CSV file
            for r, rank in enumerate(master_ranks):
                filename = f'{folder_name}{modes[m]}/runtime_r{rank}_M{num_masters}_N{NFE}_s{seed}.metric'
                # check if the file exists, if not skip it
                if not os.path.exists(filename):
                    print(f"File {filename} does not exist")
                    continue
                else:
                    runtime_bs = pd.read_csv(filename, delimiter=' ', header=0, index_col=False)
                    hvol_allseeds_allmasters[:, s, r] = runtime_bs[metric_name].values
                    hvol_allranks[:, r] = runtime_bs[metric_name].values
                
                # plot the hypervolume values
                #curr_ax.plot(np.arange(freq, NFE+freq, freq), hvol_allranks[:,r], color=seed_colors[s], linewidth=1.75, alpha=1.0)
            # at each frequency, take the maximum hypervolume across all ranks
            hvol_allseeds_min[:, s] = np.min(hvol_allranks, axis=1)
            hvol_allseeds_max[:, s] = np.max(hvol_allranks, axis=1)
            hvol_allseeds[:, s] = np.mean(hvol_allranks, axis=1)
            
            #if s == 0:
                #curr_ax.plot(np.arange(0, NFE+freq, freq), hvol_allseeds[:,s], color=seed_colors[s], linewidth=2.0, label=f'Mode: {modes[m]}')

        hvol_allseeds_allmasters_max = np.max(hvol_allseeds_allmasters, axis=2)
        hvol_allseeds_allmasters_norm = hvol_allseeds_allmasters / np.max(hvol_allseeds_allmasters_max)
        hvol_allseeds_allmasters_norm_max = np.max(hvol_allseeds_allmasters_norm, axis=2)
        hvol_allseeds_allmasters_norm_min = np.min(hvol_allseeds_allmasters_norm, axis=2)
        hvol_allseeds_allmasters_norm_mean = np.mean(hvol_allseeds_allmasters_norm, axis=2)

        print(hvol_allseeds_allmasters_norm_max.shape)
        
        # plot the hypervolume range
        curr_ax.fill_between(np.arange(freq, NFE+freq, freq), np.min(hvol_allseeds_allmasters_norm_min, axis=1),
                              np.max(hvol_allseeds_allmasters_norm_max, axis=1),
                                color=mode_colors[m], alpha=0.2)
        # plot the mean hypervolume
        curr_ax.plot(np.arange(freq, NFE+freq, freq), np.mean(hvol_allseeds_allmasters_norm_mean, axis=1), color=mode_colors[m], linewidth=2.0, label=f'Mode: {modes[m]}')
        curr_ax.legend(loc='lower right', fontsize=10, frameon=False)
        curr_ax.axhline(y=np.max(np.max(hvol_allseeds_allmasters_norm_max)), color=mode_colors[m], linestyle='--', linewidth=1.0, alpha=0.5)

        if m == 0:
            curr_ax.set_ylabel(metric_name)
        if n == 0:
            curr_ax.set_title(mode_names[m])
            #curr_ax.set_ylim([0.5, 0.9])
        #if n == 0:
        curr_ax.set_xlabel('x1000 NFE')
        curr_ax.set_xticks(np.arange(freq, NFE+freq+1, 20*freq).astype(int))
        #label xtick with scientific notation
        xtick_labels = (np.arange(freq, NFE+freq+1, 20*freq)/1000).astype(int)
        curr_ax.set_xlim([freq, NFE+freq])
        curr_ax.set_xticklabels(xtick_labels)
        curr_ax.set_ylim([0.5, 1.0])

        # remove top and right spines
        curr_ax.spines['top'].set_visible(False)
        curr_ax.spines['right'].set_visible(False)
        #else:
            #curr_ax.set_xticks(np.arange(freq, NFE+freq, 1000*freq))
            #curr_ax.set_xticklabels([])

plt.tight_layout()
plt.savefig(f'temp_figures/rel_hvol_base_IU_fullExp_range.png')