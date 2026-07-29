import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
import statsmodels.api as sm
from helper_functions_objs import *

# to be changed by the user
output_figure_filename = 'figures/dvs_IU_base_hist_triggersnd.pdf'

# create decision variable files with headers 
dv_names = ['RT_W', 'RT_D', 'RT_F', 'TT_D', 'TT_F', 'LMA_W', 'LMA_D', 'LMA_F', \
    'AP_W', 'AP_D', 'AP_F', 'IT_W', 'IT_D', 'IT_F', 'IP_W', 'IP_D', 'IP_F', \
    'INF_W', 'INF_D', 'INF_F', 'NRR_W', 'CRL', 'CRH', 'WR1', 'SCR', 'GQR', \
    'NRR_F', 'WR2_W', 'WR2_D', 'WR2_F']

dv_base_filename = '../../results/DU Optimization/dvs_base_nd_truncated_extremes.csv'
dv_iu_filename = '../../results/DU Optimization/dvs_IU_nd_truncated_extremes.csv'

trigger_names = ['RT_W', 'INF_W', 'RT_D', 'TT_D', 'INF_D', 'RT_F', 'TT_F', 'INF_F']
alloc_names = ['LMA_W', 'LMA_D', 'LMA_F', 'AP_W', 'AP_D', 'AP_F']
dvs_relevant = trigger_names + alloc_names
infra_W = ['NRR_W', 'CRL', 'CRH', 'WR1', 'GQR', 'WR2_W']
infra_D = ['SCR', 'WR2_D']
infra_F = ['NRR_F', 'WR2_F']

util_abbrevs = ['W', 'D', 'F']
util_names_dict = {'W': 'Watertown', 'D': 'Dryville', 'F': 'Fallsland'}

num_dvs = len(dv_names)

# import decision variable files 
dv_iu = pd.read_csv(dv_iu_filename, index_col=None, header=None)
dv_base = pd.read_csv(dv_base_filename, index_col=None, header=None)

# replace column headers with abbreviated names
dv_iu.columns = dv_names
dv_base.columns = dv_names

dv_IU_triggers = dv_iu[trigger_names]
dv_base_triggers = dv_base[trigger_names]
dvs_base_relevant = dv_base[dvs_relevant]
dvs_IU_relevant = dv_iu[dvs_relevant]
infra_W_triggers_IU = dv_iu[infra_W]
infra_D_triggers_IU = dv_iu[infra_D]   
infra_F_triggers_IU = dv_iu[infra_F]
infra_W_triggers_base = dv_base[infra_W]
infra_D_triggers_base = dv_base[infra_D]
infra_F_triggers_base = dv_base[infra_F]

# normalize the decision variables
dv_iu_norm = (dv_iu - dv_iu.min()) / (dv_iu.max() - dv_iu.min())
dv_base_norm = (dv_base - dv_base.min()) / (dv_base.max() - dv_base.min())

# create a 2 x 4 subplot to plot distribution of each decision variable
fig, axes = plt.subplots(3, 3, figsize=(9, 9))
axes = axes.flatten()

for i, dv in enumerate(trigger_names):
    ax = axes[i]
    if i > 1:
        ax = axes[i+1]
    plot_kde(dv_base_triggers, dv, f'{dv}', ax, '#6B8F71', 'base', spec_sols=False, linestyle='solid')
    plot_kde(dv_IU_triggers, dv, f'{dv}', ax, '#F1A45D', 'IU', spec_sols=False, linestyle='solid')

# plot the legend where the last subplot was removed
handles, labels = axes[0].get_legend_handles_labels()
# insert legend in the center of the figure
fig.legend(handles, labels, loc='lower center', fontsize=14, frameon=False, ncol=2, bbox_to_anchor=(0.5, -0.05))
plt.tight_layout()
plt.savefig(output_figure_filename)
