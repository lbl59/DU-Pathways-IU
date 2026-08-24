#!/bin/bash
#SBATCH --job-name="condition_demands"
#SBATCH --output="logs/condition_demands.out"
#SBATCH --error="logs/condition_demands.err"
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=20
#SBATCH --export=ALL
#SBATCH -t 24:00:00

OMP_NUM_THREADS=40
export OMP_NUM_THREADS

mpirun -np 40 python ./5_submit_condition_build_demands.py