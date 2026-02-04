#!/bin/bash
#SBATCH -p hybrid
#SBATCH -N 4
#SBATCH -o final_victory.txt
#SBATCH --get-user-env

echo "==========================================="
echo "HYBRID CLUSTER VALIDATION REPORT"
echo "Date: $(date)"
echo "Master Host: $(hostname)"
echo "Allocated Nodes: $SLURM_JOB_NODELIST"
echo "Total CPU Cores: $SLURM_CPUS_ON_NODE"
echo "==========================================="

