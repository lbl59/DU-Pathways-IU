import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_robustness import *

# setup attributes to be set by user
sim_mode = 'p90'
action_mode = 'IU'

num_sol_dict = {'base': 46, 'IU': 628}
sim_mode_colors = {'base': '#6B8F71', 'IU': '#F2B880'}
utilities = ['Watertown', 'Dryville', 'Fallsland']
util_abbrevs = ['W', 'D', 'F']
obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
objs_allutils = [obj_name + f'_{util_abbrev}' for util_abbrev in util_abbrevs for obj_name in obj_names]
objs_regional = [obj_name + '_R' for obj_name in obj_names]

# read in robustness 
robustness_df = pd.read_csv(f'../results/DU Reevaluation/robustness_sim_{sim_mode}_refset_{action_mode}.csv', header=0)
robustness_df_noReg = robustness_df.drop(columns=['Regional'])

# normalize robustness values to [0,1]
robustness_df_norm = (robustness_df - robustness_df.min().min()) / (robustness_df.max().max() - robustness_df.min().min())
robustness_df_norm_noReg = robustness_df_norm.drop(columns=['Regional'])

# import the high-cooperation solutions CSV 
high_coop_sols_IU = np.loadtxt(f"../objs_dvs/sol_high_coop_{action_mode}.csv").flatten().astype(int)

# select solutions from the set of high-cooperation solutions
high_coop_sols_IU = [sol for sol in high_coop_sols_IU if sol in range(len(robustness_df_noReg))]

# read in the percent perturbation data
percent_perturbation_IU_df = pd.read_csv(f"percent_degradation_max_allsols_IU_p90.csv", header=0)
cols_to_drop = [col for col in percent_perturbation_IU_df.columns if 'INPC' in col or 'PFC' in col]
max_percent_perturbation_IU_sat_df = percent_perturbation_IU_df.drop(columns=cols_to_drop)
max_percent_perturbation_IU = max_percent_perturbation_IU_sat_df.max(axis=1)

# filter out high-cooperation solutions that have higher perturbation than the baseline solution
# set a threshold for the maximum allowed perturbation
high_coop_sols_IU_filtered = [sol for sol in high_coop_sols_IU]


# Identify compromise solution using a Social Planner approach 
# find the maximum robustness values and index for each utility 
max_robutness_vals_sp = robustness_df_norm_noReg.max()
if max_robutness_vals_sp.shape != (3,):
    raise ValueError('Max robustness values shape is incorrect.')

diff_from_max = (max_robutness_vals_sp - robustness_df_norm_noReg)**2
sum_across_utils = diff_from_max.sum(axis=1)

sum_across_utils_highcoop = sum_across_utils[high_coop_sols_IU_filtered]
sp_idx = sum_across_utils.idxmin()
sp_idx_highcoop = sum_across_utils_highcoop.idxmin()

print(f'Social planner solution is solution #{sp_idx} with robustness values:\n{robustness_df_noReg.loc[sp_idx]}')

print(f'Social planner solution is solution #{sp_idx_highcoop} with robustness values:\n{robustness_df_noReg.loc[sp_idx_highcoop]}')