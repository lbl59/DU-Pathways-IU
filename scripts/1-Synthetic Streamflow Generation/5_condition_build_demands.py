import os
import sys
import numpy as np
import pandas as pd
import argparse
import pyarrow as pa
import pyarrow.parquet as pq

def check_and_create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)  

def write_to_parquet(data, directory, utility_name):
    """
    Write a DataFrame to a Parquet file.
    """
    data_colnums = np.arange(data.shape[1])
    data_colnames = [f'week_{i}' for i in data_colnums]
    data_df = pd.DataFrame(data, index=None, columns=data_colnames)
    parquet_file = os.path.join(directory, f'{utility_name}_demands.parquet')
    data_df.to_parquet(parquet_file, engine="pyarrow", 
                       index=False, compression="zstd",
                       compression_level=22)

def condition_demands(rdm, syn_dir, hist_dir, 
                      write_data=1, delete_syn=0, mode='csv'):
    utilities = ['Cary', 'Durham', 'OWASA', 'Raleigh', 'Pittsboro', 'Chatham']
    utilities_full_data = ['Cary', 'Durham', 'OWASA']
    utilities_large = ['Cary', 'Durham', 'OWASA', 'Raleigh']

    inflows = ['clayton_inflows', 'crabtree_creek_inflows', 'falls_lake_inflows', 
                    'jordan_lake_inflows', 'lake_wb_inflows', 'lillington_inflows', 
                    'little_river_raleigh_inflows', 'owasa_inflows',
                    'little_river_inflows', 'michie_inflows']
    evap = ['falls_lake_evap', 'lake_wb_evap', 'owasa_evap']
    n_weeks = 52
    n_years_demand = 0
    n_years_inflow = 0

    # import unit demands for large utilities
    print('Importing unit demands for large utilities...')
    unit_demands_dict = {}
    unit_demand_means = {}
    unit_demand_stdevs = {}

    for utility in utilities_large:
        unit_demands_dict[utility] = pd.read_csv(
            os.path.join(hist_dir, 'demands/weekly_unit_demands', f'{utility}UnitDemand.csv'), 
            index_col=None, header=None).values   # demand has shape (52, 18)
    
    n_years_demand = unit_demands_dict['Durham'].shape[1]
    
    for utility in utilities:
        unit_demand_means[utility] = pd.read_csv(os.path.join(hist_dir, 
                                                               'demands/weekly_unit_demands', 
                                                               f'{utility}_weekly_unit_demand_means.csv'), 
                                                index_col=None, header=None).values 
        unit_demand_stdevs[utility] = pd.read_csv(os.path.join(hist_dir, 
                                                                'demands/weekly_unit_demands', 
                                                                f'{utility}_weekly_unit_demand_sds.csv'),
                                                index_col=None, header=None).values
    
    # read in historical inflows and evaporation
    print('Reading historical inflows...')
    inflows_hist_dict = {}
    for inflow in inflows:
        inflows_hist_dict[inflow] = pd.read_csv(
            os.path.join(hist_dir, 'inflows', f'{inflow}.csv'), index_col=None, header=None).values 
        if n_years_inflow == 0:
            n_years_inflow = inflows_hist_dict[inflow].shape[0]   # inflow has shape (81, 52)

    # normalize unit demands
    unit_demand_norm_dict = {} 
    print('Normalizing unit demands...')
    for utility in utilities_large:
        unit_demands_u = unit_demands_dict[utility]
        if utility == "Raleigh":
            continue
        mean_demand = np.mean(unit_demands_u, axis=1, keepdims=True)
        stdev_demand = np.std(unit_demands_u, axis=1, keepdims=True, ddof=1)
        unit_demand_norm_dict[utility] = (unit_demands_u - mean_demand) / stdev_demand

    # log-transform inflows and combine Durham sources 
    log_inflow_dict = {}
    print('Log-transforming inflows and combining Durham sources...')
    for inflow in inflows:
        inflow_data = inflows_hist_dict[inflow]
        # replace zero and negative values with a small positive value
        inflow_data = np.where(inflow_data <= 0, 10e-6, inflow_data)
        log_inflow_dict[inflow] = np.log(inflow_data)
        
        if inflow == "little_river_inflows":
            inflow_michie = inflows_hist_dict['michie_inflows']
            inflow_little_river = inflows_hist_dict['little_river_inflows']
            inflow_combined = inflow_michie + inflow_little_river

            inflows_hist_dict['durham_inflows'] = inflow_combined
            inflows.append('durham_inflows')

            # replace zero and negative values with a small positive value
            inflow_combined = np.where(inflow_combined <= 0, 10e-6, inflow_combined)
            log_inflow_dict['durham_inflows'] = np.log(inflow_combined)

            # delete the individual inflow sources to avoid redundancy
            del inflows_hist_dict['michie_inflows']
            del inflows_hist_dict['little_river_inflows']
            # remove inflow names from the list
            inflows.remove('michie_inflows')
            inflows.remove('little_river_inflows') 

        elif inflow == "michie_inflows":
            continue
    
    # map the sources to utilities 
    source_to_util_map = {'Cary' : ['jordan_lake_inflows'],
                          'Durham' : ['durham_inflows'],
                          'OWASA' : ['owasa_inflows'],
                          'Raleigh' : ['falls_lake_inflows', 'lake_wb_inflows',
                                       'little_river_raleigh_inflows', 
                                       'crabtree_creek_inflows'],
                          'Pittsboro' : ['jordan_lake_inflows'],
                          'Chatham' : ['jordan_lake_inflows'],
                          'flow_gages' : ['lillington_inflows', 'clayton_inflows']}
    
    # shift log inflows to match demand series 
    print('Shifting log inflows to match demand series...')
    inflow_rows_to_match = n_years_inflow - n_years_demand
    log_flow_weekly_means = {}
    log_flow_weekly_stdevs = {}
    log_flow_weekly_means_shifted = {}
    log_flow_weekly_stdevs_shifted = {}
    normalized_log_inflows = {}
    normalized_log_inflows_shifted = {}

    for inflow in inflows:
        log_inflow = log_inflow_dict[inflow]
        log_inflow_shifted = log_inflow[inflow_rows_to_match:, :]  # last 18 years of inflow → (18,52)
        log_flow_weekly_means[inflow] = np.mean(log_inflow, axis=0)
        log_flow_weekly_stdevs[inflow] = np.std(log_inflow, axis=0, ddof=1)
        log_flow_weekly_means_shifted[inflow] = np.mean(log_inflow_shifted, axis=0)
        log_flow_weekly_stdevs_shifted[inflow] = np.std(log_inflow_shifted, axis=0, ddof=1)

        # write to csv files
        if write_data == 1:
            check_and_create_dir(os.path.join(hist_dir, 'log_inflows'))
            log_inflow_dir = os.path.join(hist_dir, 'log_inflows')

            print(f'Writing historical log {inflow} data to {log_inflow_dir}...')
            np.savetxt(os.path.join(log_inflow_dir, f'{inflow}_weekly_means.csv'),
                       log_flow_weekly_means[inflow], delimiter=',')
            np.savetxt(os.path.join(log_inflow_dir, f'{inflow}_weekly_stdevs.csv'), 
                       log_flow_weekly_stdevs[inflow], delimiter=',')
            np.savetxt(os.path.join(log_inflow_dir, f'{inflow}_weekly_means_shifted.csv'), 
                       log_flow_weekly_means_shifted[inflow], delimiter=',')
            np.savetxt(os.path.join(log_inflow_dir, f'{inflow}_weekly_stdevs_shifted.csv'), 
                       log_flow_weekly_stdevs_shifted[inflow], delimiter=',')
        
        normalized_log_inflows[inflow] = \
            (log_inflow - log_flow_weekly_means[inflow]) / log_flow_weekly_stdevs[inflow]
        normalized_log_inflows_shifted[inflow] = \
            (log_inflow - log_flow_weekly_means_shifted[inflow]) / \
                log_flow_weekly_stdevs_shifted[inflow]

    # build inflow-demand CDF and PDF
    pdf_rows = 16
    pdf_cols = 17
    # compute bin edges 
    y_vec = np.arange(-1.0*(pdf_rows/4.0)+0.5, (pdf_rows/4.0)+0.5, 0.5)
    z_vec = np.arange(-1.0*( (pdf_cols-1)/4.0)+0.5, ((pdf_cols-1)/4.0)+0.5, 0.5)

    if len(y_vec) != pdf_rows or len(z_vec) != pdf_cols-1:
        raise ValueError("PDF rows and columns do not match the expected dimensions.")
    
    # Irrigated and non-irrigated demand weeks in a year
    non_irr1 = 16
    irrig = 23  
    non_irr2 = 13

    # store pdfs and cdfs in a dictionary
    pdf_irrig_dict = {}
    pdf_non_irrig_dict = {}
    cdf_irrig_dict = {}
    cdf_non_irrig_dict = {}

    print('Building historical inflow-demand PDFs and CDFs...')
    for util in utilities_full_data:
        inflows_irrig = np.zeros((n_years_inflow, irrig), dtype=float)
        demand_irrig = np.zeros((n_years_demand, irrig), dtype=float)
        pdf_irrig = np.zeros((pdf_rows, pdf_cols), dtype=float)

        inflows_non_irrig = np.zeros((n_years_inflow, non_irr1 + non_irr2), dtype=float)
        demand_non_irrig = np.zeros((n_years_demand, non_irr1 + non_irr2), dtype=float)
        pdf_non_irrig = np.zeros((pdf_rows, pdf_cols), dtype=float) 

        source = source_to_util_map[util][0]

        # for irriation week 1-16
        for i in range(non_irr1):
            inflows_non_irrig[:, i] = normalized_log_inflows_shifted[source][:, i]
            demand_non_irrig[:, i] = unit_demand_norm_dict[util][i, :]

        # for irrigation weeks 16-39
        for i in range(irrig):
            inflows_irrig[:, i] = normalized_log_inflows_shifted[source][:, i + non_irr1]
            demand_irrig[:, i] = unit_demand_norm_dict[util][i + non_irr1, :]
        
        # for non-irrigation weeks 39-52
        for i in range(non_irr2):
            week = i + non_irr1 + irrig
            col = i + non_irr1
            inflows_non_irrig[:, col] = normalized_log_inflows_shifted[source][:, week]
            demand_non_irrig[:, col] = unit_demand_norm_dict[util][week, :]
        
        # flatten by year-then-week
        I_Irrig = inflows_irrig[-n_years_demand:, :].flatten(order='C')
        D_Irrig = demand_irrig.flatten(order='C') 
        I_nonIrrig = inflows_non_irrig[-n_years_demand:, :].flatten(order='C')
        D_nonIrrig = demand_non_irrig.flatten(order='C')

        # populate the PDFs 
        for idx in range(len(I_Irrig)):
            y_count = 0
            for y in y_vec:
                if (I_Irrig[idx] < y and I_Irrig[idx] >= y - 0.5):
                    zcount = 0
                    for z in z_vec:
                        if (D_Irrig[idx] < z and D_Irrig[idx] >= z - 0.5):
                            pdf_irrig[y_count-1, zcount-1] += 1
                            pdf_irrig[y_count-1, pdf_cols-1] += 1
                        zcount += 1
                y_count += 1
        
        # populate the PDFs for non-irrigated demands
        for idx in range(len(I_nonIrrig)):
            y_count = 0
            for y in y_vec:
                if (I_nonIrrig[idx] < y and I_nonIrrig[idx] >= y - 0.5):
                    zcount = 0
                    for z in z_vec:
                        if (D_nonIrrig[idx] < z and D_nonIrrig[idx] >= z - 0.5):
                            pdf_non_irrig[y_count-1, zcount-1] += 1
                            pdf_non_irrig[y_count, pdf_cols-1] += 1
                        zcount += 1
                y_count += 1
                        
        # store the pdfs 
        pdf_irrig_dict[util] = pdf_irrig
        pdf_non_irrig_dict[util] = pdf_non_irrig
        if util == 'Durham':
            pdf_irrig_dict['Raleigh'] = pdf_irrig
            pdf_non_irrig_dict['Raleigh'] = pdf_non_irrig
        if util == 'Cary':
            pdf_irrig_dict['Chatham'] = pdf_irrig
            pdf_non_irrig_dict['Chatham'] = pdf_non_irrig
            pdf_irrig_dict['Pittsboro'] = pdf_irrig
            pdf_non_irrig_dict['Pittsboro'] = pdf_non_irrig
        
        # calculate CDFs then transpose
        cdf_irrig = np.cumsum(pdf_irrig[:,:pdf_cols], axis=1)
        cdf_non_irrig = np.cumsum(pdf_non_irrig[:,:pdf_cols], axis=1)

        # store the cdfs
        cdf_irrig_dict[util] = cdf_irrig
        cdf_non_irrig_dict[util] = cdf_non_irrig
        if util == 'Durham':
            cdf_irrig_dict['Raleigh'] = cdf_irrig
            cdf_non_irrig_dict['Raleigh'] = cdf_non_irrig
        if util == 'Cary':
            cdf_irrig_dict['Chatham'] = cdf_irrig
            cdf_irrig_dict['Pittsboro'] = cdf_irrig
            cdf_non_irrig_dict['Chatham'] = cdf_non_irrig
            cdf_non_irrig_dict['Pittsboro'] = cdf_non_irrig
        
        # write the pdfs and cdfs to csv files
        if write_data == 1:
            # export historical pdfs and cdfs
            check_and_create_dir(os.path.join(hist_dir, 'inflow_demand_distributions'))
            distribution_dir = os.path.join(hist_dir, 'inflow_demand_distributions')
            print(f'Writing historical inflow-demand distributions to {distribution_dir}...')
            
            np.savetxt(os.path.join(distribution_dir, f'{util}_PDF_irr.csv'), 
                    pdf_irrig, delimiter=',', fmt='%d')
            np.savetxt(os.path.join(distribution_dir, f'{util}_PDF_nonirr.csv'),
                    pdf_non_irrig, delimiter=',', fmt='%d')
            np.savetxt(os.path.join(distribution_dir, f'{util}_CDF_irr.csv'),
                    cdf_irrig, delimiter=',', fmt='%d')    
            np.savetxt(os.path.join(distribution_dir, f'{util}_CDF_nonirr.csv'),
                    cdf_non_irrig, delimiter=',', fmt='%d')
            
            if util == 'Durham':   # Durham and Raleigh share inflow-demand distributions
                np.savetxt(os.path.join(distribution_dir, f'Raleigh_PDF_irr.csv'), 
                    pdf_irrig, delimiter=',', fmt='%d')
                np.savetxt(os.path.join(distribution_dir, f'Raleigh_PDF_nonirr.csv'),
                        pdf_non_irrig, delimiter=',', fmt='%d')
                np.savetxt(os.path.join(distribution_dir, f'Raleigh_CDF_irr.csv'),
                        cdf_irrig, delimiter=',', fmt='%d')    
                np.savetxt(os.path.join(distribution_dir, f'Raleigh_CDF_nonirr.csv'),
                        cdf_non_irrig, delimiter=',', fmt='%d')
            
            if util == "Cary": # Cary, Chatham, and Pittsboro share inflow-demand distributions
                utilities_small = ['Chatham', 'Pittsboro']
                for u in utilities_small:
                    np.savetxt(os.path.join(distribution_dir, f'{u}_PDF_irr.csv'), 
                               pdf_irrig, delimiter=',', fmt='%d')
                    np.savetxt(os.path.join(distribution_dir, f'{u}_PDF_nonirr.csv'),
                               pdf_non_irrig, delimiter=',', fmt='%d')
                    np.savetxt(os.path.join(distribution_dir, f'{u}_CDF_irr.csv'),
                               cdf_irrig, delimiter=',', fmt='%d')    
                    np.savetxt(os.path.join(distribution_dir, f'{u}_CDF_nonirr.csv'),
                               cdf_non_irrig, delimiter=',', fmt='%d')
        
    # begin applying historical distributions to synthetic inflows and demands
    print('Applying historical distributions to synthetic inflows and demands...')
    print('Creating synthetic demand data for RDM:', rdm)
    demand_syn_dir = os.path.join(syn_dir, f'rdm_{rdm}', 'demands')
    check_and_create_dir(demand_syn_dir)

    inflows_syn_dict = {}
    for inflow in inflows:
        inflows_syn_dir = os.path.join(syn_dir, f'rdm_{rdm}', 'inflows_syn')
        
        # combine Durham inflows from Michie and Little River
        if inflow == "durham_inflows":
            inflows_michie = pd.read_csv(
                os.path.join(inflows_syn_dir, f'michie_inflows.csv'), 
                index_col=None, header=None).values
            inflows_little_river = pd.read_csv(
                os.path.join(inflows_syn_dir, f'little_river_inflows.csv'), 
                index_col=None, header=None).values
            inflows_syn_dict[inflow] = inflows_michie + inflows_little_river
        else:
            inflows_syn_dict[inflow] = pd.read_csv(
                os.path.join(inflows_syn_dir, f'{inflow}.csv'), 
                index_col=None, header=None).values
            
    # iterate over synthetic inflows in the dictionary
    for source, matrix in inflows_syn_dict.items():
        num_reals, num_weeks_syn = matrix.shape
        W = np.zeros((num_reals, num_weeks_syn), dtype=float)
        curr_week = 0
        log_means = log_flow_weekly_means[source]
        log_stdev = log_flow_weekly_stdevs[source]
        for real in range(num_reals):
            curr_week = 0
            for w in range(num_weeks_syn):
                W[real, w] = (np.log(matrix[real, w]) - log_means[curr_week]) / log_stdev[curr_week] 
                curr_week = (curr_week + 1) % 52
        # save the normalized inflows
        inflows_syn_dict[source] = W
    
    # calculate weekly demand variation 
    print('Calculating weekly demand variation...')
    demand_variation = {} 
    true_pdfs = {}
    num_years_syn = 47
    num_demand_tiers = 15   # 16 demand tiers

    demand_tiers = [i / 2 - 3.5 for i in range(1, num_demand_tiers + 1)]  # +1 overflow tier

    for utility in utilities:
        source = source_to_util_map[utility][0]
        inflow = inflows_syn_dict[source]
        n_reals, num_weeks_syn = inflow.shape

        # allocate demand variation and pdf matrices
        dem_var_u = np.zeros((n_reals, num_weeks_syn), dtype=float)
        pdf_u = np.zeros((pdf_rows, pdf_cols), dtype=int)

        for r in range(num_reals):
            for y in range(num_years_syn + 1): 
                demand_level = 0
                for w in range(n_weeks): 
                    idx = (y * n_weeks) + w
                    flow_residual = inflow[r, idx]

                    # find the bin for the inflow residual
                    cnt = next((i for i, t in enumerate(demand_tiers) if flow_residual < t), 
                                num_demand_tiers)
                    pdf = []
                    cdf = []

                    # Select the suitable PDF and CDF 
                    week_num = w + 1 
                    if 16 < week_num < 39:
                        pdf = pdf_irrig_dict[utility]
                        cdf = cdf_irrig_dict[utility]
                    else:
                        pdf = pdf_non_irrig_dict[utility]
                        cdf = cdf_non_irrig_dict[utility]
                    
                    flows_in_bin = pdf[cnt, pdf_cols - 1] / 2 - 1

                    if flows_in_bin < 0 :
                        demand_level = 4
                    else:
                        if flows_in_bin == 0.5:
                            flows_in_bin = 1.0
                        if flows_in_bin == 0:
                            demand_level = 1
                        
                        rand_demand = np.random.rand() * flows_in_bin + 1
                        cnt2 = 0 
                        cdf_row = cdf[cnt, :]
                        while cnt2 < cdf_row.size and cdf_row[cnt2] < rand_demand:
                            cnt2 += 1
                        #cnt2 = min(cnt2, cdf_row.size - 1)
                        demand_level = min(cnt2 + 1, pdf_rows)
                    
                    dem_var_u[r, idx] = ((demand_level - 7) / 2) + (np.random.rand() * 501 / 1000)

                    if 16 < week_num < 39:
                        pdf_u[cnt, cnt2] += 1
                        pdf_u[cnt, pdf_cols - 1] += 1
            
        demand_variation[utility] = dem_var_u
        true_pdfs[utility] = pdf_u

        if write_data == 1:
            # write the demand variation and pdfs to csv files
            check_and_create_dir(os.path.join(syn_dir, f'rdm_{rdm}', 'demand_distributions'))
            demand_dir = os.path.join(syn_dir, f'rdm_{rdm}', 'demand_distributions')
            print(f'Writing synthetic demand distributions to {demand_dir}...')
            np.savetxt(os.path.join(demand_dir, f'{utility}_weekly_demand_variation.csv'), 
                    dem_var_u, delimiter=',')
            np.savetxt(os.path.join(demand_dir, f'{utility}_syn_weekly_demand_PDF.csv'),
                    pdf_u, delimiter=',', fmt='%d')

    # build synthetic demand timeseries 
    print('Building synthetic demand timeseries...')
    for util in utilities:
        annual_demands_dir = 'rdm_pwl_annual_demands'
        annual_demands_proj = pd.read_csv(
            os.path.join(annual_demands_dir, f'{util}_pwl_annual_demand_projections_mgd.csv'), 
            index_col=None, header=None).values
        
        demand_variation_u = demand_variation[util]
        demand_means_u = unit_demand_means[util]
        demand_stdevs_u = unit_demand_stdevs[util]

        n_rows, n_cols = demand_variation_u.shape   # n_reals, n_weeks
        #print(f'Shape of demand variation for {util}: ', demand_variation_u.shape)
        num_demand_years = n_cols // n_weeks
        #print('Number of synthetic years: ', num_years_syn)
        demand_syn_u = np.zeros((n_rows, n_cols))
        print(f'Shape of synthetic demand for {util}: ', demand_syn_u.shape)

        demand_projection_rdm = annual_demands_proj[:, int(rdm)]

        # Scale demand projections to MGW
        days_per_week = 7  
    
        for r in range(n_reals):
            for y in range(num_demand_years):
                for w in range(n_weeks):
                    idx = (y * n_weeks) + w
                    demand_syn_u[r, idx] = days_per_week * demand_projection_rdm[y] * \
                        (demand_variation_u[r, idx] * demand_stdevs_u[w] + demand_means_u[w])

        write_to_parquet(demand_syn_u, demand_syn_dir, util)
        
        if mode == "parquet":
            write_to_parquet(demand_syn_u, demand_syn_dir, util)
        else:
            filename = os.path.join(demand_syn_dir, f'{util}_demands.csv')
            np.savetxt(filename, demand_syn_u, delimiter=',', fmt='%.6f')
        
        print(f'Wrote synthetic demand data for {util} to {demand_syn_dir}')

    if delete_syn == 1:
        rdm_dir = os.path.join(syn_dir, f'rdm_{rdm}')
        rdm_evap_dir = os.path.join(rdm_dir, 'evaporation_syn')
        rdm_inflows_dir = os.path.join(rdm_dir, 'inflows_syn')
        # remove the synthetic evaporation files in the evaporation_syn directory
        for evap in evap:
            os.remove(os.path.join(rdm_evap_dir, f'{evap}.csv'))
        for inflow in inflows:
            os.remove(os.path.join(rdm_inflows_dir, f'{inflow}.csv'))

def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic streamflows and evaporation instances for each RDM row.")
    parser.add_argument('rdm_to_run', type=int, help="SOW to generate synthetic data for")
    parser.add_argument('syn_dir', help="Directory to write output CSV files")
    parser.add_argument('hist_dir', help="Directory containing historical inflows/evaporation subfolders")
    parser.add_argument('write_data', type=int, help="Flag to write historical and synthetic data files")
    parser.add_argument('delete_syn', type=int, default=0, help="Flag to delete synthetic data files after writing (default: 0)")
    parser.add_argument('mode', type=str, default='csv', help="Mode for writing data files (default: 'csv')")
    args = parser.parse_args()
    condition_demands(args.rdm_to_run, args.syn_dir, args.hist_dir, write_data=args.write_data, mode=args.mode)

if __name__ == '__main__':

    main()
