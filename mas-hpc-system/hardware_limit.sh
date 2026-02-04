#!/bin/bash
#SBATCH --job-name=hw_test
#SBATCH --partition=local
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=17    # <--- This is the trick! 17 is > 16.
#SBATCH --mem=41G             # <--- This is > 40G.
#SBATCH --overcommit

sleep 10
