import numpy as np 
import pandas as pd 
import os 
import sys

'''
DEMAND PROJECTIONS
------------------
Projections using trwsp 2014 report (in MGDs) 
PITTSBORO BASED ON 2019 TOWN REPORT BY CDM SMITH AND SUPPLEMENTED WITH
    CHATHAM COUNTY 2019 HAZEN + SAWYER REPORT AND ONLINE POWERBI
    CHATHAM PROJECTIONS ALSO UPDATED BASED ON THIS TOOL
'''
owasa_proj = np.array([8.1,8.3,9.0,9.7,10.2,10.8,11.3,11.9,12.4,12.9])
durham_proj = np.array([28,30.7,32.4,34.2,36.1,38.1,40,41.9,43.1,44.4])
raleigh_proj = np.array([58.2,64.4,71.3,78.2,84.8,91.3,97,102.7,108.9,115])
cary_apex_proj = np.array([20.9,25,28.8,31.9,34.8,37.3,39.2,40.8,41.2,41.4])
morrisville_proj = np.array([2.0,2.5,2.8,2.9,3.3,3.4,3.5,3.5,3.6,3.6])
pittsboro_proj = np.array([0.53,1.06,1.39,1.74,2.2,2.56,3.25,3.65,4.98,5.58])
chatham_proj = np.array([2.05,2.1,2.16,2.23,2.29,2.35,2.41,2.48,2.54,2.6])

# combine Cary and Morrisville
cary_proj = cary_apex_proj + morrisville_proj

# Constants 
NUM_PROJECTION_PERIODS = len(owasa_proj) # number of periods in the projections
HIST_DATA_DIR = './historical'
DAYS_IN_WEEK = 7
PROJECTION_FREQ = 6 # years, chosen as the interval between projection periods based on the provided data
NUM_YEARS = NUM_PROJECTION_PERIODS * PROJECTION_FREQ # total number of years in the projections

# Helper function to check if a directory exists and create it if not
def check_and_create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Helper function to interpolate projections to annual values
def interpolate_to_annual(projections, num_years, num_periods, projection_freq):
    u_proj_annual = np.zeros(num_years)
    year = 0
    for i in range(num_periods):
        if i == num_periods - 1:
            last_period = projections[-1]
            second_last_period = projections[-2]
            projection_period = last_period + (last_period - second_last_period)
            last_years = NUM_YEARS - year
            u_proj_annual[-last_years:] = \
                np.linspace(last_period, projection_period, last_years)
        else:
            u_proj_annual[year : year+projection_freq] = \
                np.linspace(projections[i], projections[i + 1], \
                    projection_freq)
            year += projection_freq-1

    return u_proj_annual
    
# Check if the demand directory exists in the historical data directory
check_and_create_dir(os.path.join(HIST_DATA_DIR, 'demands'))

# create annual demand projections directory 
check_and_create_dir(os.path.join(HIST_DATA_DIR, \
    'demands', 'annual_demand_projections'))

OUTPUT_DIR = os.path.join(HIST_DATA_DIR, 'demands',\
    'annual_demand_projections')

# create dictionary of projections
demand_projections = {
    'OWASA': owasa_proj,
    'Durham': durham_proj,
    'Raleigh': raleigh_proj,
    'Cary': cary_proj,
    'Pittsboro': pittsboro_proj,
    'Chatham': chatham_proj
}

demand_projections_annual = {}

# for each utility, interpolate the projections to annual values
for utility, projections in demand_projections.items():
    demand_projections_annual[utility] = interpolate_to_annual(
        projections, NUM_YEARS, NUM_PROJECTION_PERIODS, PROJECTION_FREQ)

# write the projections to csv files in the output directory
for utility, proj in demand_projections_annual.items():
    np.savetxt(
        os.path.join(OUTPUT_DIR,
            f'{utility}_annual_demand_projections_mgd.csv'),
        proj,
        delimiter=','
    )
    np.savetxt(
        os.path.join(OUTPUT_DIR,
            f'{utility}_annual_demand_projections_mgw.csv'),
        proj * DAYS_IN_WEEK,  # convert to MGW
        delimiter=','
    )

print('Annual demand projections written to:', OUTPUT_DIR)



