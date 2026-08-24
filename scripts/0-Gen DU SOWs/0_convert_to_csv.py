import numpy as np 
import pandas as pd
import os
import sys
# Get the command line arguments

if len(sys.argv) != 3:
    print("Usage: python ./0_convert_to_csv.py <input_file> <output_file>")
    sys.exit(1)
input_file = sys.argv[1]
output_file = sys.argv[2]

# read in the input file
data = pd.read_csv(f"{input_file}.txt", header=0, index_col=None, sep=" ")

data_names = data.columns.tolist()
data_names = data_names[1:len(data_names)]  # remove the first column which is not needed

data_df = data.iloc[:, :len(data_names)]  # keep only the columns we need
# rename the columns to the names we want
data_df.columns = data_names
data_vals = data_df.values

# save the data to the output directory as a csv file with and without header
data_df.to_csv(f'{output_file}_with_header.csv', index=False, header=True)
np.savetxt(f'{output_file}.csv', data_vals, delimiter=',')