import mpi4py
from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

N_RDMs = 200 

OMP_NUM_THREADS = 2
N_REALIZATIONS = 200
N_YEARS = 200

N_NODES = 2
N_PROCS_PER_NODE = 20
N_PROCS = int(N_PROCS_PER_NODE * N_NODES) # should be 40
N_RDMS_PER_PROC = int(N_RDMs/N_PROCS)  # should be 5
MODE = 'parquet'  # or 'csv'

for i in range(N_RDMS_PER_PROC):
    current_RDM = rank + (N_PROCS * i)

    command_run_rdm = "python ./4_combine_hist_syn_inflows_evap.py {} \
        ./synthetic ./historical {}".format(current_RDM, MODE)

    print(command_run_rdm)
    os.system(command_run_rdm)

comm.Barrier()