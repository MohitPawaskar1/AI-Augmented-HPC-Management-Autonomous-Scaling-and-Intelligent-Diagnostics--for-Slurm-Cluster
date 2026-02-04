#!/bin/bash
#SBATCH -p hybrid
#SBATCH -N 4
#SBATCH -o hybrid_results.txt

srun hostname
