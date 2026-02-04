#!/bin/bash
#SBATCH -p hybrid
#SBATCH -N 4
#SBATCH -o /storage/output/final_victory.txt

echo "==========================================="
echo "HYBRID NFS VALIDATION REPORT"
echo "Date: $(date)"
echo "Master Host: $(hostname)"
echo "Active Nodes in this Job: $SLURM_JOB_NODELIST"
echo "==========================================="

