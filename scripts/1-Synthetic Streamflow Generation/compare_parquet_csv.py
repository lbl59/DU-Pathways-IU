import numpy as np
import pandas as pd
import os
import pyarrow.parquet as pq
import pyarrow as pa

# import the csv inflow file
inflow_file = 'synthetic/rdm_0/demands/Chatham_demands'
inflows_csv = pd.read_csv(f'{inflow_file}.csv', header=None, index_col=None).values
inflows_pq_df = pd.read_parquet(f'{inflow_file}.parquet', engine="pyarrow")
inflows_pq = inflows_pq_df.values

# Compare the two DataFrames
diff = abs(inflows_csv - inflows_pq)
# if any value in the difference is greater than 1e-6, then the two files are not equal
comparison = np.all(diff < 1e-6)
if comparison:
    print("The CSV and Parquet files are equal within the tolerance.")
else:
    print("The CSV and Parquet files are NOT equal within the tolerance.")
    # Print the indices where they differ
    differing_indices = np.where(diff >= 1e-6)
    print("CSV value:", inflows_csv[differing_indices[0][0], differing_indices[0][1]])
    print("Parquet value:", inflows_pq[differing_indices[0][0], differing_indices[0][1]])


