#!/bin/bash
#SBATCH --job-name="combine_hist_syn_inflows_demand"
#SBATCH --output="logs/combine_hist_syn_inflows_demand.out"
#SBATCH --error="logs/combine_hist_syn_inflows_demand.err"
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=20
#SBATCH --export=ALL
#SBATCH -t 24:00:00

OMP_NUM_THREADS=40
export OMP_NUM_THREADS

mpirun -np 40 python ./4_submit_combine_hist_syn_inflows_evap.py