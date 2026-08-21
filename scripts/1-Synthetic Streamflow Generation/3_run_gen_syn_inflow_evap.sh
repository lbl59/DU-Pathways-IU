#!/bin/bash
#SBATCH --job-name="gen_syn_inflow_evap_10rdms"
#SBATCH --output="logs/gen_syn_inflow_evap_10rdms.out"
#SBATCH --error="logs/gen_syn_inflow_evap_10rdms.err"
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=20
#SBATCH --export=ALL
#SBATCH -t 24:00:00

OMP_NUM_THREADS=40
export OMP_NUM_THREADS

mpirun -np 40 python ./3_submit_gen_syn_inflow_evap.py