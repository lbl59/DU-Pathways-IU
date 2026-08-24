#!/bin/bash
#SBATCH --job-name="gen_annual_hist_demands"
#SBATCH --output="logs/gen_annual_hist_demands.out"
#SBATCH --error="logs/gen_annual_hist_demands.err"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --export=ALL
#SBATCH -t 24:00:00

python ./1_gen_annual_historical_demands.py 