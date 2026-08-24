#!/bin/bash
#SBATCH -A m2702 -C cpu
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=100
#SBATCH --cpus-per-task=2
#SBATCH --qos=regular
#SBATCH --job-name=reeval_sim_base_sol29_from400
#SBATCH --output=logs/reeval_sim_base_sol29_from400.out
#SBATCH --error=logs/reeval_sim_base_sol29_from400.err
#SBATCH --time=00:35:00
#SBATCH --mail-user=lbl59@cornell.edu
#SBATCH --mail-type=ALL

export OMP_NUM_THREADS=2

START="$(date +%s)"

srun -n 400 python ./full_reeval_w_ptb_base_script_v2.py 'base' 29 400
    
DURATION=$[ $(date +%s) - ${START} ]

echo ${DURATION} 