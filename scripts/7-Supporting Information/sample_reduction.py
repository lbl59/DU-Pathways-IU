#%%
import numpy as np
import pandas as pd 
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
# prevent Agg errors 
mpl.use('Agg')  # Use a non-interactive backend for matplot

# Function to compute discrepancy between two samples
def compute_cd_discrepancy(sample, stepsize):
    '''
    Space-filling measure of how uniformly the points cover the unit hypercube.
    Discrepancy values range from 0 to 1, with lower values indicating better uniformity.
    '''
    full_sample_size = sample.shape[0]
    curr_sample = sample
    curr_sample_size = full_sample_size
    num_disc = full_sample_size // stepsize
    disc_all = np.zeros(num_disc, dtype=float)

    disc_curr = stats.qmc.discrepancy(curr_sample, iterative=True)
    disc_all[0] = disc_curr

    for i in range(1, num_disc):
        if curr_sample_size > stepsize:
            curr_sample_size -= stepsize
            # randomly select rows 
            indices_selected = np.random.choice(full_sample_size, curr_sample_size, 
                                                replace=False)

            # Recompute discrepancy from scratch for the new sample
            curr_sample = sample[indices_selected, :]
            disc_updated = stats.qmc.discrepancy(curr_sample, iterative=True)
            disc_all[i] = disc_updated
            disc_curr = disc_updated
    return disc_all    

# Function to compute the Kolmogorov-Smirnov statistic
def ks_statistic(sample, stepsize):
    '''
    Determine whether the observed difference between two samples 
    is statistically significant. 

    p_val: Statistically difference between original sample and subsample 
    ks_stat: Quantifies the maximum vertical distance between the CDFs of two samples
    '''
    full_sample_size = sample.shape[0]
    num_factors = sample.shape[1]
    curr_sample_size = full_sample_size
    num_steps = full_sample_size // stepsize
    ks_stats = np.zeros((num_steps, num_factors), dtype=float)
    p_vals = np.zeros((num_steps, num_factors), dtype=float)

    for i in range(num_steps):
        if curr_sample_size > stepsize:
            curr_sample_size -= stepsize
            indices_selected = np.random.choice(full_sample_size, curr_sample_size, 
                                                replace=False)
            sub_sample = sample[indices_selected, :]

            for f in range(num_factors): 
                kstest_result = stats.kstest(sample[:, f], sub_sample[:, f])
                ks_stats[i, f] = kstest_result.statistic
                p_vals[i, f] = kstest_result.pvalue

    return ks_stats, p_vals
#%%
# Import sample data
rdm_samples = pd.read_csv('rdm_demand_pwl_period4_with_header.csv', 
                          index_col=None, header=0)
figure_name = 'rdm_demand_p4_stats'
rdm_names = rdm_samples.columns.tolist()
rdm_samples_values = rdm_samples.to_numpy()
num_samples = rdm_samples_values.shape[0]
num_factors = rdm_samples_values.shape[1]
stepsize = 50

p_val_threshold = 0.05
ks_val_threshold = 0.1

# normalize each column of the samples
rdm_samples_values_norm = (rdm_samples_values - rdm_samples_values.min(axis=0)) / \
    (rdm_samples_values.max(axis=0) - rdm_samples_values.min(axis=0)) 

discrepancy_values = compute_cd_discrepancy(rdm_samples_values_norm, stepsize)
ks_stats, p_vals = ks_statistic(rdm_samples_values_norm, stepsize)

# Set up color scheme for factors
colors = plt.cm.tab10(np.linspace(0, 1, num_factors))

# Map original names to display names
name_mapping = {
    'Durham': 'Dryville',
    'Cary': 'Watertown',
    'Raleigh': 'Fallsland'
}

print(discrepancy_values)

#%%
# Filter for only Durham, Cary, and Raleigh
factors_to_plot = ['Durham', 'Cary', 'Raleigh']
factor_indices = [i for i, name in enumerate(rdm_names) if name in factors_to_plot]

# plot discrepancy values and 
fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharex=True)
axs = axs.flatten()

# Plot 1: Cumulative Discrepancy
axs[0].plot(discrepancy_values[::-1], label='Cumulative Discrepancy', color='#2E86AB', linewidth=2)
axs[0].set_title('Cumulative Discrepancy', fontsize=14, fontweight='bold', pad=15)  
axs[0].set_ylabel(r'$\longleftarrow$ More even space-filling', fontsize=11)
axs[0].grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
min_samples_index = (num_samples - 200) // stepsize
# flip the min_samples_index to match the reversed x-axis
min_samples_index = len(discrepancy_values) - 1 - min_samples_index
axs[0].axvline(x=min_samples_index, color='#A4161A', linestyle='--', linewidth=2, label='min num. samples')

# Plot 2 & 3: KS Statistics and P-Values for each factor
for f in factor_indices:
    factor_name = rdm_names[f]
    display_name = name_mapping.get(factor_name, factor_name)
    axs[1].plot(ks_stats[:, f][::-1], label=display_name, color=colors[f], linewidth=2.0, alpha=0.8) 
    axs[2].plot(p_vals[:, f][::-1], label=display_name, color=colors[f], linewidth=2.0, alpha=0.8)

axs[1].axhline(y=ks_val_threshold, color='#A4161A', linestyle='--', linewidth=2, label='Threshold (0.1)', zorder=10)
axs[1].set_title(r'Kolmogorov-Smirnov (KS) Statistic $D_n$', fontsize=14, fontweight='bold', pad=15)
axs[1].set_ylabel(r'$\longleftarrow$ Smaller vertical diff in distr.', fontsize=11)
axs[1].grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

axs[1].legend(loc='upper right', frameon=False, fontsize=9, ncol=1, bbox_to_anchor=(1.0, 0.95))

# plot horizontal line
axs[2].axhline(y=p_val_threshold, color='#A4161A', linestyle='--', linewidth=2, label='Threshold (0.05)', zorder=10)
axs[2].set_title('P-Value from KS Test', fontsize=14, fontweight='bold', pad=15)
axs[2].set_ylabel(r'More similar distributions $\longrightarrow$', fontsize=11)
axs[2].set_xlabel('Sample Index', fontsize=12, fontweight='bold')
axs[2].grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

axs[2].legend(loc='upper right', frameon=False, fontsize=9, ncol=1, bbox_to_anchor=(1.0, 0.95))

# Set x-ticks for all plots
x_ticks = np.arange(0, len(discrepancy_values))
x_labels = np.arange(0, num_samples, stepsize) + stepsize
for ax in axs:
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')

# for each axis, remove the spines and set the limits
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.set_xlim(0, len(discrepancy_values))

    ax.tick_params(labelsize=10)


plt.tight_layout()
plt.savefig(f'figures/{figure_name}.pdf', dpi=300, bbox_inches='tight')

# %%
