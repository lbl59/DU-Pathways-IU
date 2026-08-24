# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 12:47:51 2020

Functions for plotting infrastructure pathways ala Gold et al 2022 Power and Pathways.
@author: dgold
@edited: lbl59
"""

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score 
from sklearn.metrics.pairwise import pairwise_distances_argmin
from matplotlib import pyplot as plt

def calc_num_clusters(util_data):
    silhouette_scores = []

    # test up to 3 clusters
    for k in range(1,4):
        kmeans = KMeans(init='k-means++', n_clusters = k, n_init=10)
        labels = kmeans.fit_predict(util_data)
        if k == 1:
            silhouette_scores.append(0)
        elif len(np.unique(labels)) > 1:
            silhouette_scores.append(silhouette_score(util_data, labels))  # Silhouette Score
    
    silhouette_np = np.array(silhouette_scores)
    best_k = np.argmax(silhouette_np)+1
    return best_k

def cluster_pathways(filepath, solution, utility, num_reals):
    fileloc = f'{filepath}/Pathways_s{solution}.out'
    
    # check for error when reading in the file
    # if there is an error, skip this solution
    try:
        pathways_df = pd.read_csv(fileloc, sep='\t')
    except Exception as e:
        print(f'Error reading {fileloc}: {e}')
        return None, None, None
    
    if pathways_df.empty:
        print(f'File {fileloc} is empty.')
        return None, None, None

    # reformat for clustering 
    # need an array with each row a realization and each column a different infrastructure option
    # elements are const weeks
    cluster_input = np.ones([num_reals, 13])*2344

    # loop through each realization
    for real in range(0, num_reals):
    # extract the realization
        current_real = pathways_df[pathways_df['Realization']==real]
        # find the infrastructure option (ids 0-2 are already built, 6 is off)
        for inf in [3,4,5,7,8,9,10,11,12]:
            if not current_real.empty:
                for index, row in current_real.iterrows():
                    if row['infra.']==inf:
                        cluster_input[real, inf] = row['week']

    # post process to remove inf options never constructed and normalize weeks
    # to [0-1] by dividing by total weeks, 2344
    cluster_input = cluster_input[:,[4,5,7,8,9,10,11,12]]/2344

    # extract columns for each utility
    if utility == 'watertown':
        # watertown has NRR, CRR_low, CRR_high, WR, WRII
        cluster_input = cluster_input[:,[0, 2, 3, 4, 5]]
    elif utility == 'dryville':
        # dryville has SCR, DR
        cluster_input = cluster_input[:,[1, 6]]
    else:
        # fallsland has NRR, FR
        cluster_input = cluster_input[:,[0, 7]]

    # k-means clustering
    num_clusters = calc_num_clusters(cluster_input)

    if num_clusters > 1:
        k_means = KMeans(init='k-means++', n_clusters = num_clusters, n_init=10)
        k_means_labels = k_means.fit_predict(cluster_input)
    else:
        # If only one cluster, assign all to cluster 0
        k_means_labels = np.zeros(cluster_input.shape[0], dtype=int)

    # assign each realization to a pathway, and calculate the median week
    # each infrastructure option is constructed in each cluster
    cluster_pathways = []
    cluster_medians = []
    for i in range(0, num_clusters):
        assigned = np.sum(k_means_labels == i)
        
        if assigned == 0:
            # subtract one from num_clusters to account for empty cluster
            num_clusters -= 1
            continue  # Skip clusters with zero realizations
        
        current_cluster =  cluster_input[k_means_labels==i,:]*2344
        cluster_pathways.append(current_cluster)
        current_medians = np.zeros(len(current_cluster[0,:]))
        
        for j in range(0, len(current_cluster[0,:])):
            current_medians[j]= np.median(current_cluster[:,j])

        cluster_medians.append(current_medians)

    # sort clusters by average of medians to get heavy, mod and light clusters
    cluster_means = np.zeros(len(cluster_medians))
    for i in range(0, len(cluster_medians)):
        cluster_means[i] = np.mean(cluster_medians[i])

    sorted_indices = np.argsort(cluster_means)

    # Stack the clusters in order of light, moderate, heavy using a for loop
    cluster_medians_sorted = []
    for idx in reversed(sorted_indices):
        cluster_medians_sorted.append(cluster_medians[idx])
    cluster_medians = np.vstack(cluster_medians_sorted)
    
    return num_clusters, cluster_pathways, cluster_medians

def cluster_pathways_perturbed(filepath, num_ptb, num_reals, utility_name, original_num_clusters): 
    cluster_pathways_allptb = []
    cluster_medians_allptb = []
    for p in range(num_ptb): 
        fileloc = f"{filepath}/Pathways_s{p}.out"

        pathways_df = pd.read_csv(fileloc, sep='\t', header=0)
        for c in pathways_df.columns:
            # force all values to become numeric 
            pathways_df[c] = pd.to_numeric(pathways_df[c], errors='coerce')
        # drop all NA values 
        pathways_df = pathways_df.dropna().astype(int)

        if pathways_df.empty:
            (f'File {fileloc} is empty.')

        # reformat for clustering 
        # need an array with each row a realization and each column a different infrastructure option
        # elements are const weeks
        cluster_input = np.ones([num_reals, 13])*2344

        # loop through each realization
        for real in range(0, num_reals):
            # extract the realization
            pathways_df_real = pathways_df[pathways_df['Realization']==real]
            # find the infrastructure option (ids 0-2 are already built, 6 is off)
            for inf in [3,4,5,7,8,9,10,11,12]:
                if not pathways_df_real.empty:
                    for index, row in pathways_df_real.iterrows():
                        if row['infra.']==inf:
                            cluster_input[real, inf] = row['week']

        # post process to remove inf options never constructed and normalize weeks
        # to [0-1] by dividing by total weeks, 2344
        cluster_input = cluster_input[:,[4,5,7,8,9,10,11,12]]/2344

        # extract columns for each utility
        if utility_name == 'watertown':
            # watertown has NRR, CRR_low, CRR_high, WR, WRII
            cluster_input = cluster_input[:,[0, 2, 3, 4, 5]]
        elif utility_name == 'dryville':
            # dryville has SCR, DR
            cluster_input = cluster_input[:,[1, 6]]
        else:
            # fallsland has NRR, FR
            cluster_input = cluster_input[:,[0, 7]]

        # k-means clustering
        num_clusters = calc_num_clusters(cluster_input)
        if num_clusters > original_num_clusters:
            num_clusters = original_num_clusters
            
        if num_clusters > 1:
            k_means = KMeans(init='k-means++', n_clusters = num_clusters, n_init=10)
            k_means_labels = k_means.fit_predict(cluster_input)
        else:
            # If only one cluster, assign all to cluster 0
            k_means_labels = np.zeros(cluster_input.shape[0], dtype=int)

        # assign each realization to a pathway, and calculate the median week
        # each infrastructure option is constructed in each cluster
        cluster_pathways = []
        cluster_medians = []
        for i in range(0, num_clusters):
            assigned = np.sum(k_means_labels == i)
        
            if assigned == 0:
                # subtract one from num_clusters to account for empty cluster
                num_clusters -= 1
                continue  # Skip clusters with zero realizations

            current_cluster =  cluster_input[k_means_labels==i,:]*2344
            cluster_pathways.append(current_cluster)
            current_medians_arr = np.zeros(len(current_cluster[0,:]))
            
            for j in range(0, len(current_cluster[0,:])):
                current_medians_arr[j]= np.median(current_cluster[:,j])

            cluster_medians.append(current_medians_arr)

        # sort clusters by average of medians to get heavy, mod and light clusters
        cluster_means = np.zeros(len(cluster_medians))
        for i in range(0, len(cluster_medians)):
            cluster_means[i] = np.mean(cluster_medians[i])

        sorted_indices = np.argsort(cluster_means)

        # Stack the clusters in order of light, moderate, heavy using a for loop
        cluster_medians_sorted = []
        for idx in reversed(sorted_indices):
            cluster_medians_sorted.append(cluster_medians[idx])
        cluster_medians = np.vstack(cluster_medians_sorted)

        cluster_pathways_allptb.append(cluster_pathways)
        cluster_medians_allptb.append(cluster_medians)
    
    return cluster_pathways_allptb, cluster_medians_allptb

def plot_single_pathway(cluster_medians, cluster_pathways, inf_options_idx,
                        c, cmap, ax, y_offset, plot_cbar=False):
    # get array of the infrastructure options without baseline
    inf_options_idx_no_baseline=inf_options_idx[1:]

    sorted_inf = np.argsort(cluster_medians)

    # plot heatmap of construction times
    cluster_pathways = np.rint(cluster_pathways/50)
    
    inf_im = np.zeros((50, np.shape(cluster_pathways)[1]+1))

    for k in range(1,np.shape(cluster_pathways)[1]+1) :
        for i in range(0,50):
            for j in range(0, len(cluster_pathways[:,k-1])):
                if cluster_pathways[j,k-1] == i:
                    inf_im[i,k] +=1

    ax.imshow((inf_im.T), cmap=cmap, aspect='auto', alpha = 0.60)
    
    # plot pathways
    # create arrays to plot the pathway lines. To ensure pathways have corners
    # we need an array to have length 2*num_inf_options
    pathway_x = np.zeros(len(cluster_medians)*2+2)
    pathway_y = np.zeros(len(cluster_medians)*2+2)

    # to make corners, each inf option must be in the slot it is triggered, and
    # the one after
    cluster_medians = np.rint(cluster_medians/50)
    
    for i in range(0,len(cluster_medians)):
        for j in [1,2]:
            pathway_x[(i*2)+j] = cluster_medians[sorted_inf[i]]
            pathway_y[(i*2)+j+1] = inf_options_idx_no_baseline[sorted_inf[i]]
    '''
    last_idx = len(cluster_medians)*2 + 1  # +1 to include the last point

    ax.plot(pathway_x[:last_idx], pathway_y[:last_idx] + y_offset, color=c, linewidth=5,
        alpha=.9, zorder=1)
    '''
    # end case
    pathway_x[-1] = 50

    # plot the pathway line
    ax.plot(pathway_x, pathway_y+y_offset, color=c, linewidth=4,
            alpha = 0.90, zorder=1)
    
    ax.set_xlim([0,50]) 
    # plot a horizontal colorbar
    if plot_cbar==True: 
        cbar = plt.colorbar(ax.imshow((inf_im.T), cmap=cmap, aspect='auto', alpha = 0.70), 
        ax=ax, orientation='horizontal', shrink=0.5, pad=0.05)
        cbar.set_label('Frequency')

def overlay_violin_timing_frequency(cluster_medians_allptb, infra_to_ypos, 
                                    facecolor_list, ax, 
                                    violin_width=0.8, alpha=0.9):
    
    if len(cluster_medians_allptb) == 0:
        return 
    
    # Assume a consistent number of clusters across perturbations for proper alignment 
    ref_num_clusters = cluster_medians_allptb[0].shape[0]
    num_ptb = len(cluster_medians_allptb)
    y_offsets = [-0.15, 0, 0.15]  # cluster track offsets (light, medium, heavy)

    for clust in range(ref_num_clusters):
        for infra, y in infra_to_ypos.items():
            values = []

            for p in range(num_ptb):
                cluster_medians = cluster_medians_allptb[p]
                if cluster_medians.shape[0] != ref_num_clusters:
                    # skip this perturbed realization if number of clusters doesn't match reference
                    continue
                if infra < 0 or infra >= cluster_medians.shape[1]:
                    # skip if infra index is out of bounds
                    continue

                values.append(cluster_medians[clust, infra])
            
            values = np.asarray(values, dtype=float)
            #print(f"Dimensions of values for cluster {clust}, infra {infra}: {values.shape}")
            values_years = np.rint(values / 50.0)     
            parts = ax.violinplot(values_years, positions=[y + y_offsets[clust]],
                            vert=False, widths=violin_width,
                            showmedians=False, showextrema=False)
            
            # plot a point for the median
            median_val = np.median(values_years)
            ax.plot(median_val, y + y_offsets[clust], marker='o', 
                    color='whitesmoke', alpha=0.8,
                    markersize=4, zorder=3)
            
            # Styling for aesthetics
            for pc in parts['bodies']:
                pc.set_facecolor(facecolor_list[clust])
                pc.set_edgecolor(facecolor_list[clust])
                pc.set_linewidth(2)
                pc.set_alpha(1.0)

def create_cluster_plots_single(util_meds, util_pathways, util_num_clusters, 
                         util_infra, cluster_colors, cmaps, ax, plot_cbar=False):
    """
    Plots the pathways for a given utility. The full three-utility version is 
    in create_cluster_plots().

    Parameters:
        w_meds: median values for each cluster for watertown
        d_meds: median values for each cluster for dryville
        f_meds: median values for each cluster for fallsland
        w_pathways: all pathways in each watertown cluster
        d_pathways: all pathways in each dryville cluster
        f_pathways: all pathways in each fallsland cluster
        n_clusters: number of clusters
        cluster_colors: an array of colors for each cluster
        cmaps: an array of colormaps for coloring the heatmap
        fig: a figure object for plotting
        fig_dims: an array with the number of rows and columns of subplots

        NOTE: DOES NOT SAVE THE FIGURE
    """
    # calculate number of non-empty infrastructure options in util_infra
    num_inf_options = len([x for x in util_infra if x != ''])

    #fig.text(0.5, 0.01, 'Years', ha='center', va='center')
    #fig.text(0.01, 0.5, 'Infrastructure options number', ha='center', va='center', rotation='vertical')

    y_offsets = [-0.15, 0, 0.15]

    for i in np.arange(util_num_clusters):
        plot_single_pathway(util_meds[i], util_pathways[i], np.arange(num_inf_options),
                              cluster_colors[i], cmaps[i], ax, 
                              y_offsets[i], plot_cbar=plot_cbar)
        
        
def create_cluster_plots(w_meds, d_meds, f_meds, w_pathways, d_pathways,
                         f_pathways, n_clusters, cluster_colors, cmaps, fig,
                         gspec, fig_col, plot_legend):
    """
    creates a figure with three subplots, each representing a utility

    Parameters:
        w_meds: median values for each cluster for watertown
        d_meds: median values for each cluster for dryville
        f_meds: median values for each cluster for fallsland
        w_pathways: all pathways in each watertown cluster
        d_pathways: all pathways in each dryville cluster
        f_pathways: all pathways in each fallsland cluster
        n_clusters: number of clusters
        cluster_colors: an array of colors for each cluster
        cmaps: an array of colormaps for coloring the heatmap
        fig: a figure object for plotting
        fig_dims: an array with the number of rows and columns of subplots

        NOTE: DOES NOT SAVE THE FIGURE
    """
    watertown_inf = ['Baseline', 'New River\nReservoir',
                     'College Rock\nExpansion Low',
                     'College Rock\nExpansion High', 'Water Reuse',
                     'Water Reuse II']
    dryville_inf = ['', 'Baseline', '', 'Sugar Creek\nReservoir', '', 'Water Reuse']
    fallsland_inf = ['', 'Baseline', '', 'New River\nReservoir', '', 'Water Reuse']
    
    #fig.text(0.5, 0.01, 'Years', ha='center', va='center')
    #fig.text(0.01, 0.5, 'Infrastructure options number', ha='center', va='center', rotation='vertical')

    ax1 = fig.add_subplot(gspec[0, fig_col])
    ax2 = fig.add_subplot(gspec[1, fig_col])
    ax3 = fig.add_subplot(gspec[2, fig_col])

    y_offsets = [-0.15, 0, 0.15]

    '''
    w_plot_order = np.argsort([np.mean(w_meds[0]), np.mean(w_meds[1]),
                               np.mean(w_meds[2])])
    d_plot_order = np.argsort([np.mean(d_meds[0]), np.mean(d_meds[1]),
                               np.mean(d_meds[2])])
    f_plot_order = np.argsort([np.mean(f_meds[0]), np.mean(f_meds[1]),
                              np.mean(f_meds[2])])
    '''

    for i in np.arange(n_clusters):
        plot_single_pathway(w_meds[i], w_pathways[i], np.array([0,1,2,3,4,5]),
                              cluster_colors[i], cmaps[i], ax1, 
                              y_offsets[i], plot_legend)
        
        plot_single_pathway(d_meds[i], d_pathways[i], np.array([0,1,2]),
                              cluster_colors[i], cmaps[i], ax2, 
                              y_offsets[i], plot_legend)
        
        plot_single_pathway(f_meds[i], f_pathways[i], np.array([0,1,2]),
                              cluster_colors[i], cmaps[i], ax3, 
                              y_offsets[i],  plot_legend)
        
        if fig_col == 0:
            ax1.set_ylabel('Watertown', fontsize=14)
            ax1.set_yticks(np.arange(0, 6))
            ax1.set_yticklabels(watertown_inf)
            
            ax2.set_ylabel('Dryville', fontsize=14)
            ax2.set_yticks(np.linspace(-0.65, 2.15, 6))
            ax2.set_yticklabels(dryville_inf)
            
            #ax3.set_xlabel('Challenging\nDU scenario', fontsize=14)
            ax3.set_xlabel('Original compromise', fontsize=14)
            ax3.set_ylabel('Fallsland', fontsize=14)
            ax3.set_yticks(np.linspace(-0.65, 2.15, 6))
            ax3.set_yticklabels(fallsland_inf)
            
        else:
            ax1.set_yticks(np.arange(0, 6))
            ax1.set_yticklabels(['', '', '', '', '', ''])
            
            ax2.set_yticks(np.linspace(-0.65, 2.15, 6))
            ax2.set_yticklabels(['', '', '', '', '', ''])
            
            ax3.set_yticks(np.linspace(-0.65, 2.15, 6))
            ax3.set_yticklabels(['', '', '', '', '', ''])
            
            if fig_col == 1:
                #ax3.set_xlabel('Baseline\nDU scenario', fontsize=14)
                ax3.set_xlabel('Worst Watertown\nrobustness', fontsize=14)
            
            elif fig_col == 2:
                ax3.set_xlabel('Worst Dryville\nrobustness', fontsize=14)
                
            elif fig_col == 3:
                ax3.set_xlabel('Worst Fallsland\nrobustness', fontsize=14)
    '''    
    if plot_legend:
        ax1.legend(['Light inf.', 'Moderate inf.', 'Heavy inf.'],
                   loc='upper left')
    '''
    ax1.tick_params(axis = "y", which = "both", left = False, right = False)
    
    ax2.tick_params(axis = "y", which = "both", left = False, right = False)
    
    ax3.tick_params(axis = "y", which = "both", left = False, right = False)
