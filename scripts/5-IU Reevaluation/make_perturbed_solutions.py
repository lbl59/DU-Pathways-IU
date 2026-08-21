import numpy as np 
import pandas as pd 
import os 
import sys 

print('Uploading DV file...')
dv_names = ['RT_W', 'RT_D', 'RT_F', 'TT_D', 'TT_F', 'LMA_W', 'LMA_D', 'LMA_F', \
    'AP_W', 'AP_D', 'AP_F', 'IT_W', 'IT_D', 'IT_F', 'IP_W', 'IP_D', 'IP_F', \
    'INF_W', 'INF_D', 'INF_F', 'NRR_W', 'CRL', 'CRH', 'WR1', 'SCR', 'GQR', \
    'NRR_F', 'WR2_W', 'WR2_D', 'WR2_F']
sols_dict = {'base': [29, 22, 13], 'IU':[466, 482, 377]}

mode = 'base'
objs_dvs_folder = f'objectives_dvs/dvs_reeval_perturbed/'
sols_selected = sols_dict[mode]
dv_file = f'objectives_dvs/dvs_{mode}_nd_truncated_extremes.csv'
dv_file_data = np.loadtxt(dv_file, delimiter=',', dtype=float)
dv_file_df = pd.DataFrame(dv_file_data, columns=dv_names)


print('Uploading DV perturbations...')
dv_perturbations = pd.read_csv('rdm_ranges_actions_500conf_h.csv',
                               index_col=None, header=0)
#output_folder = 'perturbed_lscomp/'
colnames = dv_perturbations.columns.tolist()

#print('Colnames in perturbations:', colnames)
num_perturbed_dvs = len(colnames)

# for each perturbation, create a new file with the perturbation applied
#for p in range(dv_perturbations.shape[0]):
for s in range(len(sols_selected)):
    sol_num = sols_selected[s]
    output_folder = f'{objs_dvs_folder}/'
    # check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    perturbed_sol = np.zeros((dv_perturbations.shape[0], dv_file_data.shape[1]))
    perturbed_dv_df = dv_file_df.copy()
    sol_to_perturb = dv_file_data[sol_num, :]
    perturbed_sol[:, :] = dv_file_data[sol_num, :]  # start with the original solution0
    
    for c, col in enumerate(colnames):
        original_dv_val = dv_file_df[col].values
        # find the index of the current colname in the dv_names list
        col_idx_in_dv_names = dv_names.index(col)

        # add perturbation from (p,c) to the original dv_file_data
        #perturbed_dv_file[:, col_idx_in_dv_names] = original_dv_val + perturbation[c]
        perturbed_sol[:, col_idx_in_dv_names] = sol_to_perturb[col_idx_in_dv_names] + dv_perturbations[col].values
        
        # clip the values to be within [0, 1]
        perturbed_sol[:, col_idx_in_dv_names] = np.clip(perturbed_sol[:, col_idx_in_dv_names], 0, 1)
    '''
    # write each row to the output file
    for p in range(dv_perturbations.shape[0]):
        ptb_filename = f'{output_folder}dvs_perturbations_{mode}_s{sol_num}_ptb{p}.csv'
        np.savetxt(ptb_filename, perturbed_sol[p, :].reshape(1,perturbed_sol.shape[1]), delimiter=',')
    '''
    #erturbed_dv_file[:, num_perturbed_dvs:] = dv_file_data[:, num_perturbed_dvs:]  # keep the rest of the columns unchanged
    # clip all values to be within [0, 1] for better performance and readability
    # perturbed_dv_file = np.clip(perturbed_dv_file, 0, 1)
    # write the perturbed data to a new file
    output_filename = f'{output_folder}dvs_perturbations_{mode}_s{sol_num}.csv'
    #perturbed_dv_file = perturbed_dv_df.to_numpy()
    np.savetxt(output_filename, perturbed_sol, delimiter=',')
