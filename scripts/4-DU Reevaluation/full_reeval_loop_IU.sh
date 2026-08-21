#!/bin/bash
#SBATCH -A m2702 -C cpu
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=50
#SBATCH --qos=regular
#SBATCH --job-name=reeval_IU_refset_redo
#SBATCH --output=logs/reeval_IU_refset_redo.out
#SBATCH --error=logs/reeval_IU_refset_redo.err
#SBATCH --time=10:00:00
#SBATCH --mail-user=lbl59@cornell.edu
#SBATCH --mail-type=ALL

START="$(date +%s)"
OMP_NUM_THREADS=4

srun python ./full_reeval_loop_IU_script.py

DURATION=$[ $(date +%s) - ${START} ]

echo ${DURATION}