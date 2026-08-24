import numpy as np
import pandas as pd 
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
# prevent Agg errors 
mpl.use('Agg')  # Use a non-interactive backend for matplot

# Function to plot 2D projection of samples
def plot_2d_projection(samples1, samples2, num_subsamples, factor_names, title=None, bins=10):
    num_factors = samples1.shape[1]
    fig, axes = plt.subplots(num_factors, num_factors, figsize=(16, 12))
    for i in range(num_factors):
        for j in range(num_factors):
            ax = axes[i, j]
            ax.scatter(samples1[:, i], samples1[:, j], s=10, alpha=0.8, label="Full set",
                       color='lightgray')
            ax.scatter(samples2[:, i], samples2[:, j],
                       s=20, color='indianred', alpha=0.8, 
                       label=f"{num_subsamples} subsamples")
            if i == num_factors - 1:
                ax.set_xlabel(f'{factor_names[i]}')
            if j == 0:
                ax.set_ylabel(f'{factor_names[j]}')
    if title:
        plt.suptitle(f'{title} with {num_subsamples} subsamples', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'figures/{title}_2d_projection_n{num_subsamples}.png', dpi=300)

# Function to plot the heatmap of the discrepancy matrix
def plot_discrepancy_heatmap(samples, num_subsamples, factor_names, 
                             range_list, title=None, bins=10):
    num_factors = samples.shape[1]
    
    # Only plot lower triangle subplots
    lower_triangle_indices = [(i, j) for i in range(num_factors) for j in range(num_factors) if j < i]
    num_plots = len(lower_triangle_indices)
    fig, axes = plt.subplots(1, num_plots, figsize=(3.5 * num_plots, 4))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)  # Increase space between subplots
    if num_plots == 1:
        axes = [axes]

    ims = []
    for idx, (i, j) in enumerate(lower_triangle_indices):
        ax = axes[idx]
        x = samples[:, i]
        y = samples[:, j]
        # Compute the 2D histogram
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins, 
            range=[range_list[i], range_list[j]])
        # Turn the heatmap into a binary matrix where 1 indicates coverage
        binary_heatmap = np.where(heatmap > 0, 1, 0)

        # Plot the binary heatmap
        im = ax.imshow(binary_heatmap.T, origin='lower', cmap='gray_r',
            extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], aspect='auto', vmin=0, vmax=1)
        ims.append(im)

        x_label = f'{factor_names[i]}'
        y_label = f'{factor_names[j]}'

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

    if title:
        plt.suptitle(f'{title} with {num_subsamples} subsamples', fontsize=16)
    
    if ims:
        fig.colorbar(ims[0], ax=axes, shrink=0.75, label='Percent Coverage',
                   orientation='horizontal', pad=0.2)

    plt.savefig(f'figures/{title}_discrepancy_heatmap_n{num_subsamples}.png', dpi=300)


# Import sample data
rdm_samples = pd.read_csv('rdm_inflows_with_header.csv', index_col=None, header=0)
rdm_samples_200 = pd.read_csv('rdm_inflows_200_with_header.csv', index_col=None, header=0)
title = 'RDM Inflows'
rdm_names = rdm_samples.columns.tolist()
rdm_samples_values = rdm_samples.to_numpy()
num_realizations = rdm_samples_values.shape[0]
num_subsamples1 = 200
num_subsamples2 = 300
num_subsamples3 = 500
# normalize the samples
rdm_samples_values_norm = (rdm_samples_values - np.min(rdm_samples_values, axis=0)) / \
                     (np.max(rdm_samples_values, axis=0) - np.min(rdm_samples_values, axis=0))
rdm_samples_values_norm_200 = (rdm_samples_200.to_numpy() - np.min(rdm_samples_200.to_numpy(), axis=0)) / \
                     (np.max(rdm_samples_200.to_numpy(), axis=0) - np.min(rdm_samples_200.to_numpy(), axis=0))

# Plot 2D projection of samples
plot_2d_projection(rdm_samples_values_norm, rdm_samples_values_norm_200, 200, rdm_names, 
                   title=title, bins=100)

# Plot heatmap of the discrepancy matrix
plot_discrepancy_heatmap(rdm_samples_values_norm, 1000,
                         rdm_names, range_list=[(0, 1)] * len(rdm_names), title=title, bins=20)
plot_discrepancy_heatmap(rdm_samples_values_norm_200, 200,
                         rdm_names, range_list=[(0, 1)] * len(rdm_names), title=title, bins=20)