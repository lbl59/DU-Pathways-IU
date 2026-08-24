import mpi4py
from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

N_RDMs = 200

OMP_NUM_THREADS = 40
N_REALIZATIONS = 200

N_NODES = 2
N_PROCS_PER_NODE = 20
N_PROCS = int(N_PROCS_PER_NODE * N_NODES) # should be 40
N_RDMS_PER_PROC = int(N_RDMs/N_PROCS)  # should be 5
WRITE_DATA = 1  # Flag to write historical and synthetic data files
DELETE_DATA = 0  # Flag to delete existing data files
MODE = 'parquet'  # or 'csv'

for i in range(N_RDMS_PER_PROC):
    current_RDM = rank + (N_PROCS * i)

    command_run_rdm = "python ./5_condition_build_demands.py \
        {} ./synthetic ./historical {} {} {}".format(current_RDM, 
                                                     WRITE_DATA,
                                                     DELETE_DATA,
                                                     MODE)

    print(command_run_rdm)
    os.system(command_run_rdm)

comm.Barrier()