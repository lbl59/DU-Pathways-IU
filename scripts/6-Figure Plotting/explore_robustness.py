import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_robustness import *

# setup attributes
sim_mode = 'p90'
num_sol_dict = {'base': 46, 'IU': 628}
yticks_max = {'avg': [0.0, 0.5, 1.0], 'p90': [0.0, 0.45, 0.90]}
sim_mode_colors = {'base': '#6B8F71', 'IU': '#F2B880'}
utilities = ['Watertown', 'Dryville', 'Fallsland']
util_abbrevs = ['W', 'D', 'F']
obj_names = ['REL', 'RF', 'INPC', 'PFC', 'WCC']
objs_allutils = [obj_name + f'_{util_abbrev}' for util_abbrev in util_abbrevs for obj_name in obj_names]
objs_regional = [obj_name + '_R' for obj_name in obj_names]

high_coop_base_solutions = 29 
high_coop_IU_solutions = 552