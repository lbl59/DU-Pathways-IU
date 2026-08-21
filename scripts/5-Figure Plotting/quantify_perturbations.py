import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 
import seaborn as sns
from SALib.analyze import delta
import warnings

from helper_functions_iu import find_regional_minimax

def calc_freq_degradation(sol_num, objs_names, objs_original_full_w_regional, objectives_perturbed):
    # select original objectives for the given solution number
    objs_original_w_regional = pd.DataFrame(objs_original_full_w_regional.iloc[sol_num,:]).T.reset_index(drop=True)
    objs_original_w_regional_arr = objs_original_w_regional.to_numpy().flatten()

    min_objs = objs_original_full_w_regional.min().values
    max_objs = objs_original_full_w_regional.max().values

    # process perturbed objectives
    objs_ptb_regional = find_regional_minimax(objectives_perturbed, objs_names)
    objs_ptb_w_regional = pd.concat([objectives_perturbed, objs_ptb_regional], axis=1) 
    objs_ptb_w_regional_arr = objs_ptb_w_regional.to_numpy()
    col_names = objs_ptb_w_regional.columns
    # calculate the frequency of degradation in each column relative to original
    # for all columns with the name "REL_", turn it negative
    # iterate over all 'REL_' columns and multiply by -1
    for c, col in enumerate(col_names):
        if "REL_" in col:
            objs_ptb_w_regional[col] = 1 - objs_ptb_w_regional[col]
            objs_ptb_w_regional_arr[:,c] = 1 - objs_ptb_w_regional_arr[:,c]

    freq_degradation = np.zeros(objs_ptb_w_regional.shape[1], dtype=int)
    percent_degradation = np.zeros((objs_ptb_w_regional.shape[0], objs_ptb_w_regional.shape[1]), dtype=float)
    percent_degradation_weighted = np.zeros((objs_ptb_w_regional.shape[0], objs_ptb_w_regional.shape[1]), dtype=float)
    # iterate over each column and count how many times perturbed > original
    for c in range(objs_ptb_w_regional_arr.shape[1]):
        objs_original_val = objs_original_w_regional_arr[c]
        # normalize the objectives by the min and max of the original objectives
        denom = max_objs[c] - min_objs[c]
        diff = objs_ptb_w_regional_arr[:, c] - objs_original_val

        # calculate number of times perturbed is greater than original
        diff_pos = np.where(diff > 0)[0]
        freq_degradation[c] = len(diff_pos)
        # calculate absolute degradation
        # since increase in objective is degradation, we multiply by -1 to imply that
        # negative percent means degradation
        if objs_original_val > 0:
            # calculate percent degradation relative to original value
            percent_degradation[:, c] = diff/objs_original_val
        elif objs_original_val == 0:  # if the original objective is zero, the percent degradation is 100
            percent_degradation[:, c] = diff/1.0   # divide by small number
        
        # weight the percent degradation by the normalized distance of the original objective from 0
        # the closer the original objective is to 0, the less impact the percent degradation has
        # if denom is nonzero, scale the percent degradation, otherwise leave as-is
        if denom > 0:
            percent_degradation_weighted[:, c] = percent_degradation[:, c] * (objs_original_val / denom)
        
        # check if percent degradation contains NaNs
        if np.isnan(percent_degradation[:, c]).any():
            warnings.warn(f'NaN values found in percent_degradation for objective {col_names[c]}')

    #percent_degradation_df = pd.DataFrame(percent_degradation, columns=objs_ptb_w_regional.columns, index=None)
    return freq_degradation, percent_degradation, percent_degradation_weighted

def calc_freq_degradation_allsols(objectives_original, objs_names, refset_name, sim_mode):
    objectives_names_full = objectives_original.columns.tolist() + ['REL_R', 'RF_R', 'INPC_R', 'PFC_R', 'WCC_R']  # extend with regional
    freq_degradation_all = np.zeros((objectives_original.shape[0], 20), dtype=int)
    percent_degradation_max = np.zeros((objectives_original.shape[0], 20), dtype=float)
    percent_degradation_median = np.zeros((objectives_original.shape[0], 20), dtype=float)
    directory = f'perturbations_{refset_name}/'

    # perform regional minimax
    objs_original_full_regional = find_regional_minimax(objectives_original, objs_names)
    objs_original_full_w_regional = pd.concat([objectives_original, objs_original_full_regional], axis=1)
    # iterate over all 'REL_' columns and multiply by -1
    for col in objs_original_full_w_regional.columns:
        if "REL_" in col:
            objs_original_full_w_regional[col] = 1 - objs_original_full_w_regional[col]

    for sol_num in range(objectives_original.shape[0]):

        sol_directory = f'{directory}sol{sol_num}_{refset_name}'

        # check if sol_directory exists
        if not os.path.isdir(sol_directory):
            continue
        objectives_perturbed = pd.read_csv(f'{sol_directory}/objs_ptb_sim_{sim_mode}_sol{sol_num}.csv', 
                                           index_col=None, header=None)
        objectives_perturbed.columns = objectives_original.columns
        
        # convert to float
        freq_degradation, percent_degradation, percent_degradation_weighted = \
            calc_freq_degradation(sol_num, objs_names, objs_original_full_w_regional, objectives_perturbed)
        freq_degradation_all[sol_num, :] = freq_degradation
        percent_degradation_df = pd.DataFrame(percent_degradation, columns=objectives_names_full, index=None)
        percent_degradation_weighted_df = pd.DataFrame(percent_degradation_weighted, columns=objectives_names_full, index=None)
        #percent_degradation_max[sol_num, :] = percent_degradation_df.max().values
        percent_degradation_max[sol_num, :] = percent_degradation_weighted_df.max().values
        percent_degradation_median[sol_num, :] = percent_degradation_weighted_df.mean().values
        #np.savetxt(f"{sol_directory}percent_degradation_sol{sol_num}_sim_{sim_mode}.csv", percent_degradation, delimiter=",")
        #percent_degradation_df.to_csv(f"{directory}/percent_degradation/sol{sol_num}_sim_{sim_mode}.csv", index=False)
        #percent_degradation_weighted_df.to_csv(f"{directory}/percent_degradation/sol{sol_num}_sim_{sim_mode}_weighted.csv", index=False)
        
    # save freq_degradation_all to csv
    freq_degradation_all_df = pd.DataFrame(freq_degradation_all, columns=objectives_names_full, index=None)
    #freq_degradation_all_df.to_csv(f'perturbations_{refset_name}/freq_degradation_allsols_{refset_name}_{sim_mode}_new.csv', index=False)
    percent_degradation_max_df = pd.DataFrame(percent_degradation_max, columns=objectives_names_full, index=None)
    #percent_degradation_max_df.to_csv(f'perturbations_{refset_name}/percent_degradation_max_allsols_{refset_name}_{sim_mode}_new.csv', index=False)
    percent_degradation_median_df = pd.DataFrame(percent_degradation_median, columns=objectives_names_full, index=None)
    percent_degradation_median_df.to_csv(f'perturbations_{refset_name}/percent_degradation_mean_allsols_{refset_name}_{sim_mode}_new.csv', index=False)

def calc_degradation_stats_allsols(objs_original_df, objs_headers, refset_name, sim_mode, save_files=False):
    # calculate the statistical measures for each objective across all perturbations 
    degradation_p90 = np.zeros((objs_original_df.shape[0], len(objs_headers)), dtype=float) # 90th percentiles 
    degradation_exp = np.zeros((objs_original_df.shape[0], len(objs_headers)), dtype=float) # mean degradation
    degradation_median = np.zeros((objs_original_df.shape[0], len(objs_headers)), dtype=float) # median degradation
    #degradation_iqr = np.zeros((objs_original_df.shape[0], len(objs_all)), dtype=float) # interquartile range
    degradation_max = np.zeros((objs_original_df.shape[0], len(objs_headers)), dtype=float) # max degradation
    #degradation_var = np.zeros((objs_original_df.shape[0], len(objs_all)), dtype=float) # variance
    for sol_num in range(objs_original_df.shape[0]):
        ptb_sol_filename = f"perturbations_{refset_name}/percent_degradation/sol{sol_num}_sim_{sim_mode}.csv"
        # import the percent degradation data
        ptb_sol_df = pd.read_csv(ptb_sol_filename, index_col=None, header=0)
        # cap all values that are greater than 1.0 to 1.0
        ptb_sol_df = ptb_sol_df.clip(upper=1.0)
        # iterate through each objective and calculate the 90th percentile
        for i, obj in enumerate(objs_headers):
            # get the nonnegative degradation values only
            pos_degradations = ptb_sol_df[obj][ptb_sol_df[obj] >= 0]
            if len(pos_degradations) > 0:
                degradation_p90[sol_num, i] = np.percentile(pos_degradations, 90)
                degradation_exp[sol_num, i] = np.mean(pos_degradations)
                degradation_median[sol_num, i] = np.median(pos_degradations)
                degradation_max[sol_num, i] = np.max(pos_degradations)
            else:
                degradation_p90[sol_num, i] = 0.0
                degradation_exp[sol_num, i] = 0.0
                degradation_median[sol_num, i] = 0.0
                #degradation_iqr[sol_num, i] = 0.0
                degradation_max[sol_num, i] = 0.0
                #degradation_var[sol_num, i] = 0.0

    # save the degradation statistics as csv files
    if save_files == True:
        degradation_median_df = pd.DataFrame(degradation_median, columns=objs_headers)
        degradation_median_df.to_csv(f'perturbations_{refset_name}/degradation_median_{refset_name}_{sim_mode}.csv', index=False)
        degradation_max_df = pd.DataFrame(degradation_max, columns=objs_headers)
        degradation_max_df.to_csv(f'perturbations_{refset_name}/degradation_max_{refset_name}_{sim_mode}_noweight.csv', index=False)
        degradation_exp_df = pd.DataFrame(degradation_exp, columns=objs_headers)
        degradation_exp_df.to_csv(f'perturbations_{refset_name}/degradation_exp_{refset_name}_{sim_mode}_noweight.csv', index=False)
        degradation_p90_df = pd.DataFrame(degradation_p90, columns=objs_headers)
        degradation_p90_df.to_csv(f'perturbations_{refset_name}/degradation_p90_{refset_name}_{sim_mode}_noweight.csv', index=False)
    
    return degradation_p90, degradation_exp, degradation_median, degradation_max

def find_bounds(input_file):
    bounds = np.zeros((input_file.shape[1],2), dtype=float)
    for i in range(input_file.shape[1]):
        bounds[i,0] = min(input_file[:,i])
        bounds[i,1] = max(input_file[:,i])

    return bounds

def check_dvs(input_file):
    # for each column, check if all more than half of the values are the same
    # this means that the column has low variability and should be removed 
    # they will return a singular matrix error in delta analysis
    cols_to_remove = []
    num_rows = input_file.shape[0]
    for i in range(input_file.shape[1]):
        col = input_file.iloc[:,i]
        most_common_value = col.mode()[0]
        count_most_common = (col == most_common_value).sum()
        if count_most_common > num_rows / 2:
            cols_to_remove.append(i)
    return cols_to_remove

def delta_sensitivity(decvar_df_selected, objs_perturbations, sol_num, bounds, sim_mode, refset_name):
    X = decvar_df_selected.to_numpy()
    Y = objs_perturbations

    dv_names_selected = decvar_df_selected.columns
    objs_names = objs_perturbations.columns

    problem = {
        'num_vars': int(decvar_df_selected.shape[1]),
        'names': dv_names_selected,
        'bounds': bounds
    }

    delta_output_dir = f'perturbations_{refset_name}/sol{sol_num}_{refset_name}/'

    for i in range(objs_perturbations.shape[1]):
        measure_label = objs_names[i]
        #print('obj: ', measure_label)
        
        filename_S1 = f'{delta_output_dir}S1_{measure_label}_{refset_name}_{sim_mode}.csv'
        filename_delta = f'{delta_output_dir}delta_{measure_label}_{refset_name}_{sim_mode}.csv'
        
        #filename = 'delta_output/delta_base_rdm/S1_' + mo_label + '_' + compSol_full + '.csv'
        # if all values in Y[measure_label] are the same, skip
        # if X has any rows with all same values, skip
        if Y[measure_label].nunique() == 1:
            #print(f"All values for {measure_label} are the same. Skipping delta analysis.")
            continue
        else:
            S1 = delta.analyze(problem, X, Y[measure_label].values, num_resamples=100, 
                               conf_level=0.95, print_to_console=False, )
            numpy_S1 = np.array(S1["S1"])
            numpy_delta = np.array(S1["delta"])
            numpy_S1_conf = np.array(S1["S1_conf"])
            numpy_delta_conf = np.array(S1["delta_conf"])

            fileout_S1 = pd.DataFrame([dv_names_selected, numpy_S1], index = None, columns = None)
            fileout_S1.to_csv(filename_S1, sep=",")

            fileout_S1_conf = pd.DataFrame([dv_names_selected, numpy_S1_conf], index = None, columns = None)
            fileout_S1_conf.to_csv(f'{delta_output_dir}S1_conf_{measure_label}_{refset_name}_{sim_mode}.csv', sep=",")

            fileout_delta = pd.DataFrame([dv_names_selected, numpy_delta], index = None, columns = None)
            fileout_delta.to_csv(filename_delta, sep=",")

            fileout_delta_conf = pd.DataFrame([dv_names_selected, numpy_delta_conf], index = None, columns = None)
            fileout_delta_conf.to_csv(f'{delta_output_dir}delta_conf_{measure_label}_{refset_name}_{sim_mode}.csv', sep=",")
    return

def gather_delta_results(sol_num, refset_name, sim_mode):
    output_dir = f'perturbations_{refset_name}/sol{sol_num}_{refset_name}/'
    #delta_files = [f for f in os.listdir(output_dir) if f.startswith('delta_') and f.endswith(f'_{refset_name}_{sim_mode}.csv')]
    #delta_conf_files = [f for f in os.listdir(output_dir) if f.startswith('delta_conf_') and f.endswith(f'_{refset_name}_{sim_mode}.csv')]
    #S1_files = [f for f in os.listdir(output_dir) if f.startswith('S1_') and f.endswith(f'_{refset_name}_{sim_mode}.csv')]
    #S1_conf_files = [f for f in os.listdir(output_dir) if f.startswith('S1_conf_') and f.endswith(f'_{refset_name}_{sim_mode}.csv')]
    
    utilities = ['_W', '_D', '_F', '_R']
    objs = ['REL', 'RF', 'INPC', 'PFC', 'WCC']

    dv_names = ['RT_W', 'RT_D', 'RT_F', 'TT_D', 'TT_F', 'INF_W', 'INF_D', 'INF_F']

    s1_dv_objs_W = np.zeros((len(objs), len(dv_names)), dtype=float)
    s1_dv_objs_D = np.zeros((len(objs), len(dv_names)), dtype=float)
    s1_dv_objs_F = np.zeros((len(objs), len(dv_names)), dtype=float)
    s1_dv_objs_R = np.zeros((len(objs), len(dv_names)), dtype=float)

    delta_dv_objs_W = np.zeros((len(objs), len(dv_names)), dtype=float)
    delta_dv_objs_D = np.zeros((len(objs), len(dv_names)), dtype=float)
    delta_dv_objs_F = np.zeros((len(objs), len(dv_names)), dtype=float)
    delta_dv_objs_R = np.zeros((len(objs), len(dv_names)), dtype=float)

    s1_dv_objs_dict = {'_W': s1_dv_objs_W, '_D': s1_dv_objs_D, '_F': s1_dv_objs_F, '_R': s1_dv_objs_R}
    s1_conf_dv_objs_dict = {'_W': s1_dv_objs_W, '_D': s1_dv_objs_D, '_F': s1_dv_objs_F, '_R': s1_dv_objs_R}
    delta_dv_objs_dict = {'_W': delta_dv_objs_W, '_D': delta_dv_objs_D, '_F': delta_dv_objs_F, '_R': delta_dv_objs_R}
    delta_conf_dv_objs_dict = {'_W': delta_dv_objs_W, '_D': delta_dv_objs_D, '_F': delta_dv_objs_F, '_R': delta_dv_objs_R}

    for u in utilities:
        s1_util = s1_dv_objs_dict[u]
        delta_util = delta_dv_objs_dict[u]
        s1_conf_util = s1_conf_dv_objs_dict[u]
        delta_conf_util = delta_conf_dv_objs_dict[u]

        for obj in objs:
            objs_util = obj + u
            curr_file_S1 = f"{output_dir}S1_{objs_util}_{refset_name}_{sim_mode}.csv"
            curr_file_S1_conf = f"{output_dir}S1_conf_{objs_util}_{refset_name}_{sim_mode}.csv"
            curr_file_delta = f"{output_dir}delta_{objs_util}_{refset_name}_{sim_mode}.csv"
            curr_file_delta_conf = f"{output_dir}delta_conf_{objs_util}_{refset_name}_{sim_mode}.csv"

            # check if files exist
            if not os.path.isfile(curr_file_S1) or not os.path.isfile(curr_file_delta):
                #print(f"Files for {objs_util} not found. Skipping...")
                continue
            else:
                S1_df = pd.read_csv(curr_file_S1, sep=',', skiprows=2, header=None).iloc[0, 1:]
                s1_util[objs.index(obj), :] = S1_df.values

                S1_conf_df = pd.read_csv(curr_file_S1_conf, sep=',', skiprows=2, header=None).iloc[0, 1:]
                s1_conf_util[objs.index(obj), :] = S1_conf_df.values
            
            if not os.path.isfile(curr_file_delta):
                #print(f"Delta file for {objs_util} not found. Skipping...")
                continue
            else:
                delta_df = pd.read_csv(curr_file_delta, sep=',', skiprows=2, header=None).iloc[0, 1:]
                delta_util[objs.index(obj), :] = delta_df.values

            if not os.path.isfile(curr_file_delta_conf):
                #print(f"Delta conf file for {objs_util} not found. Skipping...")
                continue
            else:
                delta_conf_df = pd.read_csv(curr_file_delta_conf, sep=',', skiprows=2, header=None).iloc[0, 1:]
                delta_conf_util[objs.index(obj), :] = delta_conf_df.values

        s1_util_df = pd.DataFrame(s1_util, columns=dv_names, index=None)
        s1_util_df.to_csv(f"{output_dir}s1_dv_objs{u}_{refset_name}_{sim_mode}.csv", index=False)

        s1_conf_util_df = pd.DataFrame(s1_conf_util, columns=dv_names, index=None)
        s1_conf_util_df.to_csv(f"{output_dir}s1_conf_dv_objs{u}_{refset_name}_{sim_mode}.csv", index=False)

        delta_util_df = pd.DataFrame(delta_util, columns=dv_names, index=None)
        delta_util_df.to_csv(f"{output_dir}delta_dv_objs{u}_{refset_name}_{sim_mode}.csv", index=False)

        delta_conf_util_df = pd.DataFrame(delta_conf_util, columns=dv_names, index=None)
        delta_conf_util_df.to_csv(f"{output_dir}delta_conf_dv_objs{u}_{refset_name}_{sim_mode}.csv", index=False)
    return

def plot_sensitivity_heatmap(sol_num, refset_name, sim_mode):
    utilities = ['_W', '_D', '_F', '_R']
    util_dict = {'_W': 'Watertown', '_D': 'Dryville', '_F': 'Fallsland', '_R': 'Regional'}
    objs = ['REL', 'RF', 'INPC', 'PFC', 'WCC']

    dv_names = ['$RT_{W}$', '$RT_{D}$', '$RT_{F}$', '$TT_{D}$', '$TT_{F}$', 
                '$INF_{W}$', '$INF_{D}$', '$INF_{F}$']

    data_dir = f'perturbations_{refset_name}/sol{sol_num}_{refset_name}/'

    grid_kws = {"height_ratios": (0.2, 0.2, 0.2, 0.2), "hspace": 0.4}
    fig_delta, axs_delta = plt.subplots(4,1, figsize=(8,16), gridspec_kw=grid_kws)
    axs_delta = axs_delta.flatten()
    axs_delta_cbar = fig_delta.add_axes([0.25, 0.05, 0.5, 0.02])  # [left, bottom, width, height]
    fig_s1, axs_s1 = plt.subplots(4,1, figsize=(8,16), gridspec_kw=grid_kws)
    axs_s1 = axs_s1.flatten()
    axs_s1_cbar = fig_s1.add_axes([0.25, 0.05, 0.5, 0.02])  # [left, bottom, width, height]
    cmap_col_delta = sns.color_palette("GnBu", as_cmap=True)
    cmap_col_s1 = sns.color_palette("BuPu", as_cmap=True)
    
    # Set vmin and vmax for heatmaps to scale colormaps to 0-1 range
    vmin = 0.0
    vmax = 1.0

    for u in range(len(utilities)):
        util = utilities[u]
        delta_filepath = f"{data_dir}delta_dv_objs{util}_{refset_name}_{sim_mode}.csv"
        s1_filepath = f"{data_dir}s1_dv_objs{util}_{refset_name}_{sim_mode}.csv"
        # check if files exist
        if not os.path.isfile(delta_filepath):
            print(f"Files for utility {util} not found. Skipping...")
            continue
        else:
            delta_df = pd.read_csv(delta_filepath, index_col=None)
        
            axs_delta[u] = sns.heatmap(delta_df, linewidths=.05, cmap=cmap_col_delta, 
                                   xticklabels=dv_names, yticklabels=objs, ax=axs_delta[u], 
                                   cbar=True, cbar_ax = axs_delta_cbar, cbar_kws = {'orientation': 'horizontal'},
                                   vmin=vmin, vmax=vmax)
            axs_delta[u].set_yticklabels(objs, rotation=0)
            axs_delta[u].set_xticklabels(dv_names, rotation=45, ha='right')
            axs_delta[u].set_title(f'Delta Sensitivity ({util_dict[util]})', size=14)
        # check if S1 file exists
        if not os.path.isfile(s1_filepath):
            #print(f"S1 file for utility {util} not found. Skipping...")
            continue
        else:
            s1_df = pd.read_csv(s1_filepath, index_col=None)
            axs_s1[u] = sns.heatmap(s1_df, linewidths=.05, cmap=cmap_col_s1, 
                                    xticklabels=dv_names, yticklabels=objs, ax=axs_s1[u], 
                                    cbar=True, cbar_ax = axs_s1_cbar, cbar_kws = {'orientation': 'horizontal'},
                                    vmin=vmin, vmax=vmax)
            axs_s1[u].set_yticklabels(objs, rotation=0)
            axs_s1[u].set_xticklabels(dv_names, rotation=45, ha='right')
            axs_s1[u].set_title(f'S1 Sensitivity ({util_dict[util]})', size=14)
    
    # save the figures
    fig_delta.savefig(f'figures/delta_results/delta_sensitivity_heatmap_{refset_name}_{sim_mode}_sol{sol_num}.png', bbox_inches='tight')
    fig_s1.savefig(f'figures/s1_results/s1_sensitivity_heatmap_{refset_name}_{sim_mode}_sol{sol_num}.png', bbox_inches='tight')

    # turn off showing the plots
    plt.close(fig_delta)
    plt.close(fig_s1)
    