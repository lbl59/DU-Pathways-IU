import os
import argparse
import numpy as np
import pandas as pd
from scipy.linalg import cholesky

def check_and_create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def mu_sinusoid(A, T, p, i, total_weeks):
    # Sinusoidal mean adjustment
    return 1.0 + A * np.sin(2 * np.pi * (i + np.arange(0, total_weeks, 52)) / T + p)\
          - A * np.sin(p)

def shift_matrix(M, shift):
    n_rows, n_cols = M.shape
    vec = M.flatten(order='F')
    vec_shift = vec[shift : n_rows * n_cols - shift]
    vec_shift_matrix = vec_shift.reshape((n_rows - 1, n_cols), order='C')
    return vec_shift_matrix

def gen_synthetic_matrix(hist_matrix, hist_type, random_matrix, 
                         num_syn_years, rdm_values):
    num_hist_years = hist_matrix.shape[0]
    num_weeks = hist_matrix.shape[1]
    reals_per_rdm = random_matrix.shape[0]
    min_evap_shift = 0.0
    shift = 26
    bootstrap_size = 100

    if hist_type == 'E':
        min_evap_shift = hist_matrix.min().min()
        hist_matrix = hist_matrix - min_evap_shift  # ensure non-negative evaporation
        # replace zero values with a small positive value
        hist_matrix[hist_matrix == 0] = 1e-6  # avoid log(0) issues
        # replace NaN values with a small positive value
        hist_matrix[np.isnan(hist_matrix)] = 1e-6  # avoid log(NaN) issues
        # ensure the shift is positive

    # generate synthetic data
    num_syn_weeks = num_syn_years * 52
    synthetic_matrix = np.zeros((reals_per_rdm, num_syn_weeks))

    # weekly log-mean & std
    log_mat_hist = np.log(hist_matrix)
    weekly_mean = np.mean(log_mat_hist, axis=0)
    weekly_std = np.std(log_mat_hist, axis=0)

    for real in range(reals_per_rdm):
        random_matrix_r = random_matrix[real]
        nQ = num_hist_years * bootstrap_size 
        logQ_matrix = np.tile(log_mat_hist, (bootstrap_size, 1))
        # normalize the historical data
        Z_full = ((logQ_matrix - weekly_mean) / weekly_std)
        # shift the normalized matrix
        Z_shifted_full = shift_matrix(Z_full, shift)

        # get the correlation matrix
        U = cholesky(np.corrcoef(Z_full[:num_hist_years], rowvar=False), 
                    lower=True)
        U_shifted = cholesky(np.corrcoef(Z_shifted_full[:num_hist_years-1], rowvar=False),
                    lower=True)
        Z_uncorr = Z_full[random_matrix_r.flatten(), :]

        Qs_corr = Z_uncorr.dot(U)
        Q_uncorr_vec = Z_uncorr.flatten(order='F')
        Q_uncorr_shifted_vec = Q_uncorr_vec[shift:(num_syn_years+1)*num_weeks - shift]
        Q_uncorr_shifted =  Q_uncorr_shifted_vec.reshape(
                (num_syn_years, num_weeks), order='C')    
        Qs_corr_shifted = Q_uncorr_shifted.dot(U_shifted)    

        # impose weekly mean & std
        Qs_log = np.zeros((num_syn_years, num_weeks), dtype=float)
        Qs_log[:, 0:shift] = Qs_corr_shifted[:, shift:52]
        Qs_log[:, shift:52] = Qs_corr[:num_syn_years, shift:52]

        # impose weekly mean & std
        synthetic_matrix_real = np.zeros((num_syn_years, num_weeks), dtype=float)
        for w in range(num_weeks):
            mu = mu_sinusoid(rdm_values[0], rdm_values[1], rdm_values[2],
                            w, num_weeks)
            synthetic_matrix_real[:, w] = np.exp(Qs_log[:, w] * weekly_std[w] + weekly_mean[w]*mu)
        
        synthetic_matrix[real, :] = synthetic_matrix_real.flatten(order='C')

        if hist_type == 'E':
            # Evaporation is negative, so we invert the sign
            synthetic_matrix[real, :] *= -1

    return synthetic_matrix

def stress_dynamic(random_matrix, Q_hist, E_hist, 
                   num_hist_years, num_syn_years, rdm_values, reals_per_rdm):
    """
    Generate synthetic streamflow (Qs) and evaporation (Es) series for one realization.

    random_matrix: 2D array shape ((num_years+1), 52)
    Q_hist, E_hist: dict of {location: 1D array length (n_hist_years*52)}
    rdm_row: 1D array of sinusoidal parameters [A, T, p]
    """

    syn_dict = {'Q': {}, 'E': {}}
    # Generate and correlate per label & location
    for label, hist_dict in (('Q', Q_hist), ('E', E_hist)):
        syn_dict[label] = {}
        
        for source, hist_matrix in hist_dict.items():
            syn_dict[label][source] = gen_synthetic_matrix(hist_matrix, label, random_matrix, 
                                                           num_syn_years, rdm_values)
    Qs = syn_dict['Q']
    Es = syn_dict['E']

    return Qs, Es

def generate_sample(rdm_to_run, reals_per_rdm, num_syn_years, output_dir, hist_dir):
    """
    For each row in the RDM parameter file, generate multiple (instances_per_rdm) realizations
    of synthetic inflow and evaporation series and write them to CSV.
    """
    # all filenames 
    inflow_filenames = ['clayton_inflows', 'crabtree_creek_inflows', 'falls_lake_inflows', 
                    'jordan_lake_inflows', 'lake_wb_inflows', 'lillington_inflows', 
                    'little_river_inflows', 'little_river_raleigh_inflows',
                    'michie_inflows', 'owasa_inflows']
    evap_filenames = ['falls_lake_evap', 'lake_wb_evap', 'owasa_evap']
                        
    # Load historical time series files
    print('Loading historical data...')
    Q_hist = {fname: pd.read_csv(
        os.path.join(hist_dir, 'inflows', f'{fname}.csv'), index_col=None, header=None).values
        for fname in inflow_filenames}
    E_hist = {fname: pd.read_csv(
        os.path.join(hist_dir, 'evaporation', f'{fname}.csv'), index_col=None, header=None).values * (-1)
        for fname in evap_filenames}   # negate evaporation values

    # Load RDM sinusoidal parameter table
    print('Loading RDM parameters...')
    rdm_all = pd.read_csv('rdm_inflows_200.csv', header=None).values
    num_hist_years = next(iter(Q_hist.values())).shape[0] // 52

    # Loop over each RDM parameter row
    rdm = rdm_to_run
    print(f'Generating synthetic data for RDM {rdm}...')
    
    # Generate multiple instances for this RDM
    random_matrix = np.random.randint(low=0, high=num_hist_years * 100, 
                                        size=(reals_per_rdm, (num_syn_years+1), 52))

    # check if the RDM folder exists; create if not
    rdm_folder = os.path.join(output_dir, f'rdm_{rdm}')
    rdm_values = rdm_all[int(rdm), :]
    # Ensure the output directory exists
    check_and_create_dir(rdm_folder)
    rdm_inflows_dir = os.path.join(rdm_folder, 'inflows_syn')
    rdm_evap_dir = os.path.join(rdm_folder, 'evaporation_syn')
    check_and_create_dir(rdm_inflows_dir)
    check_and_create_dir(rdm_evap_dir)
    print('Directories built!')

    # Build random index matrix for this realization
    Qs, Es = stress_dynamic(random_matrix, Q_hist, E_hist, 
                            num_hist_years, num_syn_years, 
                            rdm_values, reals_per_rdm)
    print(f'Calculated synthetic inflows and evaporation for rdm_{rdm}!')

    # Write out each series with unique filename
    print('Writing synthetic inflows and evaporation to CSV files...')
    for source_inflow, matrix_inflow in Qs.items():
        np.savetxt(os.path.join(rdm_inflows_dir, f"{source_inflow}.csv"),
                    matrix_inflow, delimiter=',')
    
    for source_evap, matrix_evap in Es.items():
        np.savetxt(os.path.join(rdm_evap_dir, f"{source_evap}.csv"),
                    matrix_evap, delimiter=',')

def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic streamflows and evaporation instances for each RDM row.")
    parser.add_argument('rdm_to_run', type=int, help="SOW to generate synthetic data for")
    parser.add_argument('reals_per_rdm', type=int, help="number of realizations per SOWs")
    parser.add_argument('num_syn_years', type=int, help="Number of synthetic years to generate")
    parser.add_argument('output_dir', type=str, help="Directory to write output CSV files")
    parser.add_argument('hist_dir', type=str, help="Directory containing historical inflows/evaporation subfolders")
    args = parser.parse_args()
    generate_sample(args.rdm_to_run, args.reals_per_rdm, args.num_syn_years, args.output_dir, args.hist_dir)


if __name__ == '__main__':

    main()
