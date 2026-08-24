from mpi4py import MPI
import numpy as np
import os
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"Rank {rank} of {size} is starting...")

N_RDMs = 200
N_REALIZATIONS = 200
N_PTB = 100
OMP_NUM_THREADS = 2

DATA_DIR = "/pscratch/sd/l/lbl59/WaterPaths-IU/"
MODE = sys.argv[1] if len(sys.argv) > 1 else "IU"  # Default to "test" if no argument is provided
SOL_NUM = sys.argv[2] if len(sys.argv) > 2 else "622"  # Default to "622" if no argument is provided
PTB_OFFSET = int(sys.argv[3]) if len(sys.argv) > 3 else 0  # Default to "0" if no argument is provided
SOLS_FILE_NAME = f"objectives_dvs/dvs_reeval_perturbed/dvs_perturbations_{MODE}_s{SOL_NUM}.csv"
 
# Generate all (ptb, rdm) pairs
ptb_ids = list(range(N_PTB))
work_items = [(ptb+PTB_OFFSET, rdm) for ptb in ptb_ids for rdm in range(N_RDMs)]
my_items = np.array_split(work_items, size)[rank]

# Assign each rank a unique work item
for current_ptb, current_RDM in my_items:
    output_dir =f"full_reeval_perturbations_{MODE}/sol{SOL_NUM}_rdm{current_RDM}/"
    #output_dir_old = f"full_reeval_perturbations_{MODE}/sol{SOL_NUM}_rdm{current_RDM}/"
    if not os.path.exists(output_dir):
        # if the old file does not exists, assume the output doesn't exist and run the command
        os.makedirs(output_dir)

    command_run_rdm = "./SedentoValleySimulation -T {} -t 2344 -r {} \
        -d {} -D TestFiles/DU_SOWs -R {} \
        -C -1 -O rof_tables_reeval_base/rdm_{}/\
        -v {} -s {} -f {} -l {} -p 1 -M 1 \
        -U TestFiles/rdm_utilities_test_problem_reeval_200v2.csv \
        -P TestFiles/rdm_dmp_test_problem_reeval_200v2.csv \
        -W TestFiles/rdm_water_sources_test_problem_reeval_200v2.csv".format(
                                OMP_NUM_THREADS, N_REALIZATIONS, DATA_DIR, 
                                current_RDM, current_RDM, output_dir, 
                                SOLS_FILE_NAME, current_ptb, current_ptb+1)

    os.system(command_run_rdm)

comm.Barrier()
