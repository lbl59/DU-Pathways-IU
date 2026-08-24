import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns
from helper_functions_objs import *

# create decision variable files with headers 
dv_names = ['RT_W', 'RT_D', 'RT_F', 'TT_D', 'TT_F', 'LMA_W', 'LMA_D', 'LMA_F', \
    'AP_W', 'AP_D', 'AP_F', 'IT_W', 'IT_D', 'IT_F', 'IP_W', 'IP_D', 'IP_F', \
    'INF_W', 'INF_D', 'INF_F', 'NRR_W', 'CRL', 'CRH', 'WR1', 'SCR', 'GQR', \
    'NRR_F', 'WR2_W', 'WR2_D', 'WR2_F']

dv_base_filename = 'objectives_dvs_nd/dvs_base_nd_truncated_extremes.csv'
dv_iu_filename = 'objectives_dvs_nd/dvs_IU_nd_truncated_extremes.csv'

trigger_names = ['RT_W', 'RT_D', 'RT_F', 'TT_D', 'TT_F','INF_W', 'INF_D', 'INF_F']
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

# plot the figure 
# Utilities and triggers (Watertown only has RT and INF as requested)
utils = ['W', 'D', 'F']
utils_dict = {'W': 'Watertown', 'D': 'Dryville', 'F': 'Fallsland'}
triggers_per_util = {
    'W': ['RT_W', 'INF_W'],
    'D': ['RT_D', 'TT_D', 'INF_D'],
    'F': ['RT_F', 'TT_F', 'INF_F'],
}

# Solutions to plot: baseline + IU high-coop solutions
#base_idx = base_sp[0]            # e.g., 36

solutions = [
    ('Social Planner', 401),
    ('Baseline', 29),
]

# Colors: use your color dicts already defined in the notebook
color_map = {
    'Social Planner':  '#B66D0D',
    'Baseline': "#425E46"
}
    

# Figure & axes
fig, axs = plt.subplots(1, len(utils), figsize=(8, 2.5), sharex=True)
axs = axs.flatten() if isinstance(axs, np.ndarray) else [axs]
if not isinstance(axs, (list, np.ndarray)):
    axs = [axs]

for i, util in enumerate(utils):
    ax = axs[i]
    triggers = triggers_per_util[util]
    n_tr = len(triggers)
    n_sol = len(solutions)

    # y positions = one row per trigger; we'll offset bars for each solution inside each group
    y = np.arange(n_tr)
    total_group_height = 0.8
    bar_height = total_group_height / n_sol
    offsets = (np.arange(n_sol) - (n_sol - 1) / 2.0) * bar_height

    # Plot each solution (one set of bars per solution)
    for j, (label, sol_idx) in enumerate(solutions):
        vals = []
        for t in triggers:
            if label == 'baseline':
                raw = dv_base_triggers.iloc[sol_idx][t]
            else:
                raw = dv_IU_triggers.iloc[sol_idx][t]
            v = 1.0 - raw             # keep original 1.0 - dv logic

            vals.append(v)

        y_pos = y + offsets[j]
        ax.barh(y_pos, vals, height=bar_height * 0.92, color=color_map.get(label, 'lightgrey'), label=label)

    # labels and style
    ax.set_yticks(y)
    ax.set_yticklabels([t.split('_')[0] for t in triggers])
    ax.set_title(utils_dict[util])
    if i == len(utils) - 1:
        ax.set_xlabel(r"Increased use $\longrightarrow$")
    ax.invert_yaxis()  # optional: put first trigger at top; remove if you prefer bottom-up
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Shared legend below
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.025))
fig.tight_layout(rect=[0, 0.08, 1, 1])
# Save/show
plt.savefig('supporting_fig4.pdf', dpi=300, bbox_inches='tight')
plt.show()