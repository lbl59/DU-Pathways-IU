import numpy as np 
import pandas as pd 
import os
import sys

# Get the command line arguments
if len(sys.argv) != 3:
    print("Usage: python ./2_gen_annual_pwl_syn_demands.py <num_rdm> <output_dir>")
    sys.exit(1)

# Helper function to check if a directory exists and create it if not
def check_and_create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Define constants
HIST_DATA_DIR = './historical'
DEMAND_PROJ_DIR = os.path.join(HIST_DATA_DIR, 'demands', 'annual_demand_projections')
NUM_RDM = int(sys.argv[1])
OUTPUT_DIR = sys.argv[2]   # rdm_pwl_annual_demands

check_and_create_dir(HIST_DATA_DIR)
check_and_create_dir(OUTPUT_DIR)

# check that user has created the demand projections 
if not os.path.exists(DEMAND_PROJ_DIR):
    print(f"Error: The directory {DEMAND_PROJ_DIR} does not exist. "
          "Please run 1_gen_annual_historical_demands.py first.")
    sys.exit(1)

# import the multipliers 
multipliers_period1 = pd.read_csv('rdm_demand_pwl_period1_200_with_header.csv',index_col=None, header=0)
multipliers_period2 = pd.read_csv('rdm_demand_pwl_period2_200_with_header.csv',index_col=None, header=0)
multipliers_period3 = pd.read_csv('rdm_demand_pwl_period3_200_with_header.csv',index_col=None, header=0)
multipliers_period4 = pd.read_csv('rdm_demand_pwl_period4_200_with_header.csv',index_col=None, header=0)

utilities = ['OWASA', 'Durham', 'Raleigh', 'Cary', 'Pittsboro', 'Chatham']

def calc_growth(y, annual_demand, rdm_demand, multiplier):
    #growth_diff = demand[y] - demand[y - 1]
    #demand_y = demand[y] + (growth_diff * multiplier)
    # if the multiplier is negative, it means the demand is decreasing
    diff = abs(annual_demand[y] - annual_demand[y - 1]) * multiplier
    demand_y = rdm_demand[y - 1] + diff
    return demand_y

def calc_growth2(diff, rdm_demand, multiplier):
    # rate of growth between two years
    demand_y = rdm_demand + (diff * multiplier)
    return demand_y

# for each utility, create a matrix  of demands 
for utility in utilities:
    print(f'Processing {utility}...')
    annual_demand_proj = np.loadtxt(
        os.path.join(DEMAND_PROJ_DIR, f'{utility}_annual_demand_projections_mgd.csv')).flatten()
    
    num_years = len(annual_demand_proj)
    period1_mult = multipliers_period1[utility].values
    period2_mult = multipliers_period2[utility].values
    period3_mult = multipliers_period3[utility].values
    period4_mult = multipliers_period4[utility].values

    annual_demand_proj_rdm = np.zeros((num_years, NUM_RDM))

    # anchor the first year of the projections to the historical data
    annual_demand_proj_rdm[0, :] = annual_demand_proj[0]

    for rdm in range(NUM_RDM):
        for y1 in range(1, num_years // 4):
            '''annual_demand_proj_rdm[y1, rdm] = calc_growth2(diff1, annual_demand_proj_rdm[y1-1, rdm], 
                                                          period1_mult[rdm])
            '''
            annual_demand_proj_rdm[y1, rdm] = calc_growth(y1, annual_demand_proj, 
                                                          annual_demand_proj_rdm[:, rdm], 
                                                          period1_mult[rdm])
            
        for y2 in range(num_years // 4, num_years // 2):
            '''annual_demand_proj_rdm[y2, rdm] = calc_growth2(diff2, annual_demand_proj_rdm[y2-1, rdm], 
                                                          period2_mult[rdm])
            '''
            annual_demand_proj_rdm[y2, rdm] = calc_growth(y2, annual_demand_proj, 
                                                          annual_demand_proj_rdm[:, rdm], 
                                                          period2_mult[rdm])
        for y3 in range(num_years // 2, 3 * num_years // 4):
            '''annual_demand_proj_rdm[y3, rdm] = calc_growth2(diff3, annual_demand_proj_rdm[y3-1, rdm], 
                                                          period3_mult[rdm])
            '''
            annual_demand_proj_rdm[y3, rdm] = calc_growth(y3, annual_demand_proj, 
                                                          annual_demand_proj_rdm[:, rdm], 
                                                          period3_mult[rdm])
        for y4 in range(3 * num_years // 4, num_years):
            '''annual_demand_proj_rdm[y4, rdm] = calc_growth2(diff4, annual_demand_proj_rdm[y4-1, rdm], 
                                                          period4_mult[rdm])
            '''
            annual_demand_proj_rdm[y4, rdm] = calc_growth(y4, annual_demand_proj, 
                                                          annual_demand_proj_rdm[:, rdm], 
                                                          period4_mult[rdm])
    
    # save the matrix to a csv file
    np.savetxt(
        os.path.join(OUTPUT_DIR, f'{utility}_pwl_annual_demand_projections_mgd.csv'),
        annual_demand_proj_rdm, delimiter=',', fmt='%.12f'
    )