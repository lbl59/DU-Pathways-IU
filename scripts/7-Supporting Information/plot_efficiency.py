import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
sns.set_style('whitegrid')
 
# define constants 
num_seeds = 1
NFE = 5000
num_masters = 2

#num_procs = [256, 512, 1024]
num_procs = [256, 512, 1024]
num_proc_labels = ['64', '128', '256']  # Corresponding labels for the number of processors
num_procs_per_master = [int((n-num_masters) / num_masters) for n in num_procs]  # Calculate number of processors per master
print(num_procs_per_master)
time_to_5000 = [31350, 570, 296, 151]
nfe_in_30_parallel = [15500, 30000, 59500]
nfe_in_30_serial = 140
efficiency = [nfe_p /(nfe_in_30_serial * p) for nfe_p, p in zip(nfe_in_30_parallel, num_procs_per_master)]

# plot the efficiency over number of processors
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(num_procs, efficiency, marker='o', linestyle='-', color='#195165', linewidth=4.0, 
        markersize=15, markerfacecolor='white', markeredgewidth=3.0, markeredgecolor='#195165')
ax.set_xticks(num_procs)  # Set x-ticks to the number of processors
ax.set_xticklabels(num_proc_labels, fontsize=12)  # Use the corresponding labels for
ax.set_xlabel(r'Number of Processors, $n$', fontsize=14)
ax.set_ylabel(r"Efficiency, $E=\frac{NFE_p}{n\times NFE_s}$", fontsize=14)
ax.set_title('Efficiency of Parallel Execution using 5,000 NFE\n(2 jobs per processor)', fontsize=18, pad=20)

ax.set_ylim([0.6, 1.0])  # Set y-axis limits to better visualize efficiency
ax.set_yticks(np.arange(0.6, 1.05, 0.1))
ax.set_yticklabels([f'{y}%' for y in np.arange(60, 105, 10)], fontsize=12)  # Convert to percentage labels
ax.set_xlim([0, 1100])
ax.set_xticks(np.arange(0, 1100, 200))  # Set x-ticks to the number of processors for clarity
ax.set_xticklabels(np.arange(0, 275, 50), fontsize=12)

# remove top and right spines for better aesthetics
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# remove vertical grid lines
ax.xaxis.grid(False)
plt.savefig('Efficiency_plot_new.png', dpi=300, bbox_inches='tight')
