import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

import seaborn as sns

# plot historgram of decision variables
def plot_histogram(df, dv, title, ax, color, setup):
    data_dv = df[dv]
    data_dv_df = pd.DataFrame(data_dv, columns=[dv])
    sns.histplot(data=data_dv_df, ax=ax, kde=False, color=color, label=setup)
    ax.set_title(title)
    ax.set_xlabel('Decision Variable Value')
    ax.set_ylabel('Frequency')
    ax.grid(False)
    ax.legend_.remove()

def plot_kde(df, dv, title, ax, color, setup,
             spec_sols=False, spec_sol_num=None, spec_sol_colors=None,
             linestyle='--'):
    data_dv = df[dv]
    data_dv_df = pd.DataFrame(data_dv, columns=[dv])
    sns.kdeplot(data=data_dv_df, x=dv, ax=ax, color=color, 
                fill=False, linewidth=2, label=setup, common_norm=True)
    
    ax.set_title(title)
    ax.set_xlabel('Decision Variable Value')
    ax.set_ylabel('Density')
    ax.grid(False)

    if spec_sols == True:
        for s, sol in enumerate(spec_sol_num):
            sol_value = df[dv].iloc[sol]
            ax.axvline(sol_value, color=spec_sol_colors[s], linestyle=linestyle, linewidth=1)

    # remove right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

def plot_cdf(df, dv, title, ax, color, setup):
    data_dv = df[dv]
    ax.ecdf(data_dv, color=color, label=setup, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(r'$\longleftarrow$ Increasing DV use')
    ax.set_ylabel('Prob. of occurence')
    ax.grid(False)

def find_sols(dv_df, sol_type, dv_thresholds):
    sols_selected = []
    if sol_type=="high_coop":
        dv_threshold_low = dv_thresholds[0]
        # find solutions where the infrastructure and transfer triggers for all utilities are high 
        sols_selected = dv_df[(dv_df['INF_W'] < dv_threshold_low) & 
                          (dv_df['INF_F'] < dv_threshold_low) & 
                          (dv_df['TT_D'] < dv_threshold_low) & 
                          (dv_df['TT_F'] < dv_threshold_low)]
    elif sol_type=="low_coop":
        dv_threshold_high = dv_thresholds[0]
        # find solutions where the infrastructure and transfer triggers for all utilities are low 
        sols_selected = dv_df[(dv_df['INF_W'] > dv_threshold_high) & 
                          (dv_df['INF_F'] > dv_threshold_high) & 
                          (dv_df['TT_D'] > dv_threshold_high) & 
                          (dv_df['TT_F'] > dv_threshold_high)]
    elif sol_type=="med_coop":
        dv_threshold_low = dv_thresholds[0]
        dv_threshold_high = dv_thresholds[1]
        sols_selected = dv_df[(((dv_df['INF_W'] >= dv_threshold_low) & (dv_df['INF_W'] <= dv_threshold_high)) +
                          ((dv_df['INF_F'] >= dv_threshold_low) & (dv_df['INF_F'] <= dv_threshold_high))) +
                          (((dv_df['TT_D'] >= dv_threshold_low) & (dv_df['TT_D'] <= dv_threshold_high)) +
                          ((dv_df['TT_F'] >= dv_threshold_low) & (dv_df['TT_F'] <= dv_threshold_high)))]
    return sols_selected.index.tolist()

def plot_polar(decision_vars_IU, decision_vars_base, dv_names, utility, ax):
    # get the first letter of the utility name
    print(f'Plotting polar plot for {utility} utility')
    util_abbrev = utility[0]
    dvs_labels = ['IU', 'base']
    dvs_colors = {'IU':"#FA824C", 'base': "#7EB2DD"}

    dv_names = [f'{d}_{util_abbrev}' for d in dv_names]

    dvs_full_dict = {'IU': decision_vars_IU, 'base': decision_vars_base}

    dvs_all_cols = decision_vars_IU.columns.tolist()

    for dvs in dvs_labels:
        decision_vars = dvs_full_dict[dvs]

        # create a list of trigger names if the dv name contains T 
        dv_triggers_idx = [i for i, name in enumerate(dvs_all_cols) if \
                           (('T' in name or 'INF' in name) and f'_{util_abbrev}' in name)]
        dv_alloc_idx = [i for i, name in enumerate(dvs_all_cols) if \
                        (('T' not in name and 'INF' not in name) and f'_{util_abbrev}' in name)]
        print(f'{dvs} trigger indices: {dv_triggers_idx}')
        print(f'{dvs} allocation indices: {dv_alloc_idx}')
        
        dv_triggers = 1 - decision_vars.iloc[:,dv_triggers_idx].values
        dv_alloc = decision_vars.iloc[:,dv_alloc_idx].values
        # normalize dv_alloc to be between 0 and 1
        dv_alloc = (dv_alloc - dv_alloc.min(axis=0)) / (dv_alloc.max(axis=0) - dv_alloc.min(axis=0))
        
        # concatenate the two arrays
        dv_toplot_arr = np.concatenate((dv_triggers, dv_alloc), axis=1)
        dv_toplot_arr = np.concatenate((dv_toplot_arr, dv_toplot_arr[:,0].reshape(dv_toplot_arr.shape[0], 1)), axis=1)
        #dvs_full_toplot[dvs] = dv_toplot_arr

        # plot each decision variable on the polar plot 
        theta = np.linspace(0,2*np.pi, dv_toplot_arr.shape[1])
        for i in range(0, dv_toplot_arr.shape[0]):
            ax.plot(theta, dv_toplot_arr[i,:], color=dvs_colors[dvs], alpha=0.8)
            if i == 0:
                ax.plot(theta, dv_toplot_arr[i,:], color=dvs_colors[dvs], alpha=0.8, label=dvs)

        lines, labels = ax.set_thetagrids(range(0, 360, int(360/len(dv_names))), (dv_names))
    
    ax.set_yticklabels([])
    ax.set_title(f'{utility} DVs', va='bottom')

def plot_polar_selected_dvs(decision_vars_all, dvs_selected, dvs_color_dict, dv_names, utility, ax):
    # get the first letter of the utility name
    util_abbrev = utility[0]

    dv_names_u = [f'{d}_{util_abbrev}' for d in dv_names]
    # create a list of trigger names if the dv name contains T 
    dv_triggers_idx = [c for c in dv_names_u if ('T' in c or 'INF' in c)]
    dv_alloc_idx = [c for c in dv_names_u if ('T' not in c and 'INF' not in c)]
    
    dv_triggers = 1 - decision_vars_all.loc[:,dv_triggers_idx].values
    #dv_triggers = decision_vars_all.iloc[:,dv_triggers_idx].values
    dv_alloc = decision_vars_all.loc[:,dv_alloc_idx].values
    # normalize dv_alloc to be between 0 and 1
    dv_alloc = (dv_alloc - dv_alloc.min(axis=0)) / (dv_alloc.max(axis=0) - dv_alloc.min(axis=0))
    
    # concatenate the two arrays
    dv_toplot_arr = np.concatenate((dv_triggers, dv_alloc), axis=1)
    dv_toplot_arr = np.concatenate((dv_toplot_arr, dv_toplot_arr[:,0].reshape(dv_toplot_arr.shape[0], 1)), axis=1)

    # plot each decision variable on the polar plot 
    theta = np.linspace(0,2*np.pi, dv_toplot_arr.shape[1])
    for i in range(0, dv_toplot_arr.shape[0]):
        ax.plot(theta, dv_toplot_arr[i,:], color='lightgrey', alpha=0.8)
        if i == 0:
            ax.plot(theta, dv_toplot_arr[i,:], color='lightgrey', 
                    alpha=0.8, label='all_dvs')
    
    for j in range(0, len(dvs_selected)):
        sol_num = dvs_selected[j]
        sol_color = list(dvs_color_dict.values())[j]
        sol_type = list(dvs_color_dict.keys())[j]

        if utility == 'Watertown':
            print('Adding legend label')
            #ax.plot(theta, dv_toplot_arr[sol_num,:], color=sol_color, alpha=1.0, label=sol_type, linewidth=2.5)
            ax.bar(theta + (j%3)*0.1, dv_toplot_arr[sol_num,:], color=sol_color, 
                   alpha=1.0, label=sol_type, width=0.1, bottom=0.0, zorder=700)
        else:
            #ax.plot(theta, dv_toplot_arr[sol_num,:], color=sol_color, alpha=1.0, linewidth=2.5)
            ax.bar(theta + (j%3)*0.1, dv_toplot_arr[sol_num,:], color=sol_color, 
                   alpha=1.0, width=0.1, bottom=0.0, zorder=700)
    
    ax.set_thetagrids(range(0, 360, int(360/len(dv_names_u))), (dv_names_u))
    
    ax.set_yticklabels([])
    ax.set_title(f'{utility} DVs', va='bottom')

def plot_polar_families(decision_vars_all, dvs_selected, dvs_color_dict, dv_names, utility, ax):
    # get the first letter of the utility name
    util_abbrev = utility[0]
    dv_names_u = [f'{d}_{util_abbrev}' for d in dv_names]
    #print('DV names for utility: ', dv_names_u)
    # create a list of trigger names if the dv name contains T 
    dv_triggers_idx = [c for c in dv_names_u if ('T' in c or 'INF' in c)]
    dv_alloc_idx = [c for c in dv_names_u if ('T' not in c and 'INF' not in c)]
    
    dv_triggers = 1 - decision_vars_all.loc[:,dv_triggers_idx].values
    dv_alloc = decision_vars_all.loc[:,dv_alloc_idx].values
    # normalize dv_alloc to be between 0 and 1
    dv_alloc = (dv_alloc - dv_alloc.min(axis=0)) / (dv_alloc.max(axis=0) - dv_alloc.min(axis=0))
    
    # concatenate the two arrays
    dv_toplot_arr = np.concatenate((dv_triggers, dv_alloc), axis=1)
    dv_toplot_arr = np.concatenate((dv_toplot_arr, dv_toplot_arr[:,0].reshape(dv_toplot_arr.shape[0], 1)), axis=1)

    dv_toplot_lowcoop = dv_toplot_arr[dvs_selected['low_coop'], :]
    dv_toplot_highcoop = dv_toplot_arr[dvs_selected['high_coop'], :]
    
    # plot each decision variable on the polar plot 
    theta = np.linspace(0,2*np.pi, dv_toplot_arr.shape[1])
    for i in range(0, dv_toplot_arr.shape[0]):
        ax.plot(theta, dv_toplot_arr[i,:], color='lightgrey', alpha=0.8)
        if i == 0:
            ax.plot(theta, dv_toplot_arr[i,:], color='lightgrey', 
                    alpha=0.8, label='all_dvs')
    
    # plot each decision variable on the polar plot 
    for i in range(0, dv_toplot_highcoop.shape[0]):
        ax.plot(theta, dv_toplot_highcoop[i,:], color=dvs_color_dict['high_coop'], alpha=0.8)
        if i == 0:
            ax.plot(theta, dv_toplot_highcoop[i,:], color=dvs_color_dict['high_coop'], 
                    alpha=0.8, label='High Co-op', linewidth=2.5)
            
    # plot each decision variable on the polar plot 
    for i in range(0, dv_toplot_lowcoop.shape[0]):
        ax.plot(theta, dv_toplot_lowcoop[i,:], color=dvs_color_dict['low_coop'], alpha=0.8)
        if i == 0:
            ax.plot(theta, dv_toplot_lowcoop[i,:], color=dvs_color_dict['low_coop'], 
                    alpha=1.0, label='Low Co-op', linewidth=2.5)
    
    ax.set_thetagrids(range(0, 360, int(360/len(dv_names_u))), (dv_names_u))
    
    ax.set_yticklabels([])
    ax.set_title(f'{utility} DVs', va='bottom')

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

def calc_robustness(directory, filename, obj_regional, objs_allutils):
    # get the data
    df_sol = pd.read_csv(f'{directory}/{filename}', index_col=None, header=None)
    df_sol.columns = objs_allutils
    # find the regional minimax values
    objs_reg_df = find_regional_minimax(df_sol, obj_regional)
    # robustness defined as REL > 0.98, RF < 0.2, and WCC < 0.1
    util_abbrevs = ['W', 'D', 'F']
    robustness_arr = np.zeros(len(util_abbrevs)+1, dtype=float)
    for u, util_abbrev in enumerate(util_abbrevs):
        objs_util = [f'REL_{util_abbrev}', f'RF_{util_abbrev}', f'WCC_{util_abbrev}']
        # check if the solution meets the robustness criteria
        robust_mask = (df_sol[objs_util[0]]>= 0.98) & (df_sol[objs_util[1]] <= 0.2) & (df_sol[objs_util[2]] <= 0.05)
        robustness_arr[u] = robust_mask.sum() / robust_mask.shape[0]
    
    # regional robustness
    objs_util = ['REL_R', 'RF_R', 'WCC_R']
    robust_mask = (objs_reg_df[objs_util[0]]>= 0.98) & (objs_reg_df[objs_util[1]] <= 0.2) & (objs_reg_df[objs_util[2]] <= 0.05)
    robustness_arr[-1] = robust_mask.sum() / robust_mask.shape[0]
    
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
    
    ax.set_yticks(np.arange(0.0, 0.81, 0.4))
    ax.set_yticklabels(np.arange(0, 81, 40, dtype=int), fontsize=11)
    ax.set_ylabel(f'{utility}\nRobustness (%)')
