#!/bin/bash
#SBATCH -A m2702 -C cpu
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=50
#SBATCH --qos=debug
#SBATCH --job-name=reeval_base_avg_refset_redo
#SBATCH --output=logs/reeval_base_avg_refset_redo.out
#SBATCH --error=logs/reeval_base_avg_refset_redo.err
#SBATCH --time=00:30:00
#SBATCH --mail-user=lbl59@cornell.edu
#SBATCH --mail-type=ALL

START="$(date +%s)"

srun python ./full_reeval_loop_base_script.py

DURATION=$[ $(date +%s) - ${START} ]

echo ${DURATION}