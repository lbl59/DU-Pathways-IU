import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_iu import *
from quantify_perturbations import *

obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
util_abbrevs = ['W', 'D', 'F']

# append obj names to util_abbrevs
objs_utils = [f'{obj}_{util}' for util in util_abbrevs for obj in obj_names]
objs_regional =  [f'{obj}_R' for obj in obj_names]
objs_W = [f'{obj}_W' for obj in obj_names]
objs_D = [f'{obj}_D' for obj in obj_names]
objs_F = [f'{obj}_F' for obj in obj_names]

# to change based on the solution being analyzed
refset_name = 'IU'
sim_mode = 'p90'
sols_to_analyze = {'IU':[401], 'base':[29]}  # sol indices for each refset
colors_per_sol = {'IU': ['#B66D0D'], 'base': ['#39563D']}
objs_original_df = pd.read_csv(f'objectives_{refset_name}_{sim_mode}_nd.csv', index_col=None, header=None)
objs_original_df.columns = objs_utils
objs_original_regional_df = find_regional_minimax(objs_original_df, obj_names)
objs_original_w_regional_df = pd.concat([objs_original_df, objs_original_regional_df], axis=1)


# for each solution, perform DMSA 
for sol_num in sols_to_analyze[refset_name]:
    directory = f'perturbations_{refset_name}/sol{sol_num}_{refset_name}/'
    dv_arr = np.loadtxt(f'perturbations_{refset_name}/sol{sol_num}_{refset_name}/dvs_perturbations_{refset_name}_s{sol_num}.csv', delimiter=',')
    dv_names = ['RT_W', 'RT_D', 'RT_F', 'TT_D', 'TT_F', 'LMA_W', 'LMA_D', 'LMA_F', \
        'AP_W', 'AP_D', 'AP_F', 'IT_W', 'IT_D', 'IT_F', 'IP_W', 'IP_D', 'IP_F', \
        'INF_W', 'INF_D', 'INF_F', 'NRR_W', 'CRL', 'CRH', 'WR1', 'SCR', 'GQR', \
        'NRR_F', 'WR2_W', 'WR2_D', 'WR2_F']
    dv_names_selected = ['RT_W', 'RT_D', 'RT_F', 'TT_D', 'TT_F','INF_W', 'INF_D', 'INF_F']

    decvar_df = pd.DataFrame(dv_arr, columns=dv_names, index=None)
    decvar_df_selected = decvar_df[dv_names_selected]
    decvar_arr_selected = decvar_df_selected.to_numpy()

    cols_to_remove = check_dvs(decvar_df_selected)
    # if cols to remove is not empty, drop those columns
    if cols_to_remove:
        col_names_to_remove = [dv_names_selected[i] for i in cols_to_remove]
        decvar_df_selected.drop(columns=col_names_to_remove, inplace=True)
        decvar_arr_selected = decvar_df_selected.to_numpy()

    bounds = find_bounds(decvar_arr_selected)

    objs_perturbations = pd.read_csv(f'{directory}/objs_ptb_sim_{sim_mode}_sol{sol_num}.csv', index_col=None, header=None)
    objs_perturbations.columns = objs_utils
    objs_perturbations_regional = find_regional_minimax(objs_perturbations, obj_names)
    objs_perturbations_w_regional = pd.concat([objs_perturbations, objs_perturbations_regional], axis=1)

    # perform sensitivity analysis
    # output is written to a folder f'perturbations_{refset_name}/sol{sol_num}_{refset_name}/'
    delta_sensitivity(decvar_df_selected, objs_perturbations_w_regional, sol_num, bounds, sim_mode, refset_name)
