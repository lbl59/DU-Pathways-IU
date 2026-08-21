import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns

def find_regional_minimax(objs_df, obj_names):
    objs_reg = np.zeros((objs_df.shape[0], len(obj_names)), dtype=float)
    obj_names_regional = [f'{obj}_R' for obj in obj_names]
    for i, obj in enumerate(obj_names):
        if obj == "REL":
            REL_cols = [col for col in objs_df.columns if col.startswith('REL')]
            max_across_cols = objs_df[REL_cols].values.min(axis=1)
            objs_reg[:, i] = max_across_cols
        else:
            obj_cols = [col for col in objs_df.columns if col.startswith(obj)]
            # find the minimax value for each objective function
            objs_reg[:, i] = objs_df[obj_cols].values.max(axis=1)

    objs_reg_df = pd.DataFrame(objs_reg, columns=obj_names_regional)
    return objs_reg_df

def convert_to_df(objs_filename, objs_header):
    objs_np = np.loadtxt(objs_filename, delimiter=',', dtype=float)
    objs_df = pd.DataFrame(objs_np, columns=objs_header)
    return objs_df

def calc_robustness(directory, filename, obj_regional, objs_allutils, robustness_criteria):
    # get the data
    df_sol = pd.read_csv(f'{directory}/{filename}', index_col=None, header=None)
    df_sol.columns = objs_allutils
    # find the regional minimax values
    objs_reg_df = find_regional_minimax(df_sol, obj_regional)
    # robustness defined as REL > 0.95, RF < 0.1, and WCC < 0.1
    util_abbrevs = ['W', 'D', 'F']
    robustness_arr = np.zeros(len(util_abbrevs)+1, dtype=float)
    for u, util_abbrev in enumerate(util_abbrevs):
        objs_util = [f'REL_{util_abbrev}', f'RF_{util_abbrev}', f'WCC_{util_abbrev}']
        # check if the solution meets the robustness criteria
        robust_mask = (df_sol[objs_util[0]]>=robustness_criteria[0]) & (df_sol[objs_util[1]]<=robustness_criteria[1]) & (df_sol[objs_util[2]]<=robustness_criteria[2])
        #robustness_arr[u] = robust_mask.sum() / robust_mask.shape[0]
        robustness_arr[u] = robust_mask.sum() / 200.0
    
    # regional robustness
    objs_util = ['REL_R', 'RF_R', 'WCC_R']
    robust_mask = (objs_reg_df[objs_util[0]]>=robustness_criteria[0]) & (objs_reg_df[objs_util[1]]<=robustness_criteria[1]) & (objs_reg_df[objs_util[2]]<=robustness_criteria[2])
    #robustness_arr[-1] = robust_mask.sum() / robust_mask.shape[0]
    robustness_arr[-1] = robust_mask.sum() / 200.0
    
    return robustness_arr

def plot_robustness_bar(robustness_base, robustness_IU, utility, ax, color_dict, sols_to_highlight=None):
    robustness_base_u = robustness_base[utility].values
    robustness_IU_u = robustness_IU[utility].values
    # arrange the data in descending order of robustness
    robustness_base_sorted = np.sort(robustness_base_u)[::-1]
    robustness_IU_sorted = np.sort(robustness_IU_u)[::-1]

    width = 1.0  # the width of the bars
    # create a bar plot of robustness values where height is robustness
    ax.bar(np.arange(len(robustness_IU_sorted)), robustness_IU_sorted, width=width, 
           label='Implementation Uncertainty', color=color_dict['IU'], alpha=0.8)
    ax.bar(np.arange(len(robustness_base_sorted))+0.5, robustness_base_sorted, width=width, 
           label='Base', color=color_dict['base'], alpha=0.9)
    # turn the right and top axes invisible 
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ### TODO: highlight specific solutions
    
    ax.set_yticks(np.arange(0.0, 1.01, 0.4))
    ax.set_yticklabels(np.arange(0, 101, 40, dtype=int), fontsize=9)
    ax.set_ylabel(f'Robustness (%)')

def plot_robustness_bar_coop(robustness_base, robustness_IU, utility, ax, 
                             color_dict, sols_to_highlight=None):
    robustness_base_u = robustness_base[utility].values
    robustness_IU_u = robustness_IU[utility].values
    # arrange the data in descending order of robustness
    robustness_base_sorted = np.sort(robustness_base_u)[::-1]
    robustness_IU_sorted = np.sort(robustness_IU_u)[::-1]

    width = 1.0 # the width of the bars
    # create a bar plot of robustness values where height is robustness
    ax.bar(np.arange(len(robustness_IU_sorted)), robustness_IU_sorted, width=width, 
           label='Implementation Uncertainty', color=color_dict['IU'], alpha=0.2)
    ax.bar(np.arange(len(robustness_base_sorted))+0.5, robustness_base_sorted, width=width, 
           label='Base', color=color_dict['base'], alpha=0.2)
    
    # if sols_to_highlight is not None, highlight those solutions
    if sols_to_highlight is not None:
        sols_base_high = sols_to_highlight['base_high_coop']
        sols_base_low = sols_to_highlight['base_low_coop']
        sols_IU_high = sols_to_highlight['IU_high_coop']
        sols_IU_low = sols_to_highlight['IU_low_coop']

        for sol in sols_IU_low:
            robustness_value = robustness_IU_u[sol]
            robustness_idx = np.where(robustness_IU_sorted == robustness_value)[0][0]
            ax.bar(robustness_idx, robustness_value, width=width*4, color=color_dict['IU_low_coop'], alpha=1.0)
        for sol in sols_IU_high:
            # find indices of solution in the sorted array
            robustness_value = robustness_IU_u[sol]
            robustness_idx = np.where(robustness_IU_sorted == robustness_value)[0][0]
            ax.bar(robustness_idx, robustness_value, width=width*4, color=color_dict['IU_high_coop'], alpha=1.0)

        for sol in sols_base_low:
            robustness_value = robustness_base_u[sol]
            robustness_idx = np.where(robustness_base_sorted == robustness_value)[0][0]
            ax.bar(robustness_idx+0.5, robustness_value, width=width*4, color=color_dict['base_low_coop'], alpha=1.0)

        for sol in sols_base_high:
            robustness_value = robustness_base_u[sol]
            robustness_idx = np.where(robustness_base_sorted == robustness_value)[0][0]
            ax.bar(robustness_idx+0.5, robustness_value, width=width*4, color=color_dict['base_high_coop'], alpha=1.0)
    # turn the right and top axes invisible 
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_ylabel(f'{utility}\nRobustness (%)')
