import numpy as np
import pandas as pd
import sys
import os
import argparse
import pyarrow as pa
import pyarrow.parquet as pq

def write_to_parquet(data, directory, source_name):
    """
    Write a DataFrame to a Parquet file.
    """
    
    data_colnums = np.arange(data.shape[1])
    data_colnames = [f'week_{i}' for i in data_colnums]
    cols = [pa.array(data[:, i]) for i in range(data.shape[1])]
    table = pa.Table.from_arrays(cols, names=data_colnames)
    pq.write_table(table, os.path.join(directory, f'{source_name}.parquet'),
                   compression='zstd', compression_level=6)
    '''
    data_df = pd.DataFrame(data, index=None, columns=data_colnames)
    parquet_file = os.path.join(directory, f'{source_name}.parquet')
    data_df.to_parquet(parquet_file, engine="pyarrow", 
                       index=False, compression="snappy")
    '''


def combine_hist_syn(rdm, output_dir, hist_dir, mode='csv'):
    weeks_to_copy = np.array([0, 1, 364, 728, 1092, 1456, 1768, 
                            2132, 2496, 2860, 3172, 3536, 3900, 
                            4264, 4576, 4940])
    
    '''
    COMBINE EVAPORATION TIMESERIES
    '''
    evap_filenames = ['falls_lake_evap', 'lake_wb_evap', 'owasa_evap']
    evap_filenames_out = ['durham_evap', 'falls_lake_evap', 'little_river_raleigh_evap', 
                          'jordan_lake_evap', 'lake_wb_evap']

    hist_evap_dir = os.path.join(hist_dir, 'evaporation')
    evap_mapper = np.array([2, 0, 0, 2, 1])

    for e in range(len(evap_filenames_out)):
        print(f"Processing evaporation file: {evap_filenames_out[e]}")
        evap_hist_name = evap_filenames[evap_mapper[e]]
        HI = np.loadtxt(os.path.join(hist_evap_dir, f'{evap_hist_name}.csv'), 
                        delimiter=',')
        num_hist_years = HI.shape[0]
        HI_long = HI[num_hist_years - 50:, :]   # get the last 50 years
        HI_long_vec = HI_long.flatten(order='C')
        
        rdm_dir = os.path.join(output_dir, f'rdm_{rdm}')
        if not os.path.exists(rdm_dir):
            print(f"RDM directory {rdm_dir} does not exist. Create it first using\
                3_gen_syn_inflow_evap.py")
            continue
        rdm_evap_dir = os.path.join(rdm_dir, 'evaporation_syn')
        rdm_evap_dir_combined = os.path.join(rdm_dir, 'evaporation')
        if not os.path.exists(rdm_evap_dir_combined):
            os.makedirs(rdm_evap_dir_combined)

        SI = np.loadtxt(os.path.join(rdm_evap_dir, f'{evap_hist_name}.csv'), 
                        delimiter=',')
        n_reals = SI.shape[0]
        HI_tile = np.tile(HI_long_vec, (n_reals, 1))
        SI_full = np.hstack((HI_tile, SI))
        # add weeks to account for historical evaporation

        for w in sorted(weeks_to_copy, reverse=True):
            SI_full = np.insert(SI_full, w+1, SI_full[:, w], axis=1)
        if mode == 'parquet':
            write_to_parquet(SI_full, rdm_evap_dir_combined, evap_filenames_out[e])
        else:   
            np.savetxt(os.path.join(rdm_evap_dir_combined, f'{evap_filenames_out[e]}.csv'), 
                    SI_full, delimiter=',', fmt='%.6f')
    
    '''
    COMBINE INFLOW TIMESERIES
    '''
    inflow_filenames = ['clayton_inflows', 'crabtree_creek_inflows', 'falls_lake_inflows', 
                    'jordan_lake_inflows', 'lake_wb_inflows', 'lillington_inflows', 
                    'little_river_inflows', 'little_river_raleigh_inflows',
                    'michie_inflows', 'owasa_inflows']
    
    hist_inflows_dir = os.path.join(hist_dir, 'inflows')

    for inflow in inflow_filenames:
        print(f"Processing inflow file: {inflow}")
        HI = np.loadtxt(os.path.join(hist_inflows_dir, f'{inflow}.csv'), delimiter=',')
        num_hist_years = HI.shape[0]
        HI_long = HI[num_hist_years - 50:, :]   # get the last 50 years
        HI_long_vec = HI_long.flatten(order='C')

        rdm_dir = os.path.join(output_dir, f'rdm_{rdm}')
        if not os.path.exists(rdm_dir):
            print(f"RDM directory {rdm_dir} does not exist. Create it first using\
                3_gen_syn_inflow_evap.py")
            continue
        rdm_inflows_dir = os.path.join(rdm_dir, 'inflows_syn')
        rdm_inflows_dir_combined = os.path.join(rdm_dir, 'inflows')
        
        if not os.path.exists(rdm_inflows_dir_combined):
            os.makedirs(rdm_inflows_dir_combined)

        SI = np.loadtxt(os.path.join(rdm_inflows_dir, f'{inflow}.csv'), delimiter=',')
        n_reals = SI.shape[0]
        HI_tile = np.tile(HI_long_vec, (n_reals, 1))
        SI_full = np.hstack((HI_tile, SI))  # append historical inflows to synthetic inflows
        # add weeks to account for historical inflows
        for w in sorted(weeks_to_copy, reverse=True):
            SI_full = np.insert(SI_full, w+1, SI_full[:, w], axis=1)

        if inflow == "owasa_inflows":
            "Saving inflows for OWASA, cane creek, university lake, and stone quarry"
            cane_creek_inflows = SI_full * 31.4
            university_lake_inflows = SI_full * 28.7
            stone_quarry_inflows = SI_full * 1.2

            if mode == 'parquet':
                write_to_parquet(cane_creek_inflows, rdm_inflows_dir_combined, 'cane_creek_inflows')
                write_to_parquet(university_lake_inflows, rdm_inflows_dir_combined, 'university_lake_inflows')
                write_to_parquet(stone_quarry_inflows, rdm_inflows_dir_combined, 'stone_quarry_inflows')
                write_to_parquet(SI_full, rdm_inflows_dir_combined, 'owasa_inflows')
            else:
                np.savetxt(os.path.join(rdm_inflows_dir_combined, 'cane_creek_inflows.csv'), 
                            cane_creek_inflows, delimiter=',', fmt='%.6f')
                np.savetxt(os.path.join(rdm_inflows_dir_combined, 'university_lake_inflows.csv'), 
                            university_lake_inflows, delimiter=',', fmt='%.6f')
                np.savetxt(os.path.join(rdm_inflows_dir_combined, 'stone_quarry_inflows.csv'), 
                            stone_quarry_inflows, delimiter=',', fmt='%.6f')
                np.savetxt(os.path.join(rdm_inflows_dir_combined, 'owasa_inflows.csv'),
                            SI_full, delimiter=',', fmt='%.6f')

        elif inflow == "little_river_inflows":
            if mode == 'parquet':
                write_to_parquet(SI_full, rdm_inflows_dir_combined, 'durham_inflows')
            else:
                np.savetxt(os.path.join(rdm_inflows_dir_combined, 'durham_inflows.csv'), 
                            SI_full, delimiter=',', fmt='%.6f')

        else:
            if mode == 'parquet':
                write_to_parquet(SI_full, rdm_inflows_dir_combined, inflow)
            else:
                np.savetxt(os.path.join(rdm_inflows_dir_combined, f'{inflow}.csv'), 
                            SI_full, delimiter=',', fmt='%.6f')
    
# get args from command line 
def main():
    parser = argparse.ArgumentParser(description='Combine historical and synthetic inflows and evap.')
    parser.add_argument('rdm_to_run', type=int, help='Synthetic SOW to combine historical data for')
    parser.add_argument('output_dir', help="Directory to write output CSV files")
    parser.add_argument('hist_dir', help="Directory containing historical inflows/evaporation subfolders")
    parser.add_argument('mode', type=str, default='csv', help='Output mode: csv or parquet (default: csv)')
    args = parser.parse_args()
    combine_hist_syn(args.rdm_to_run, args.output_dir, args.hist_dir, 
                     mode=args.mode)

if __name__ == '__main__':

    main()