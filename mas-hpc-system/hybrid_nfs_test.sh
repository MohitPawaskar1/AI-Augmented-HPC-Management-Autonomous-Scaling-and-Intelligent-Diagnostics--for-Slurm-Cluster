#!/bin/bash
#SBATCH -p cloud
#SBATCH -N 1
#SBATCH -o /storage/output/hybrid_victory.txt

echo "--- Hybrid Execution Report ---"
echo "Job running on: $(hostname)"
echo "Reading from NFS: $(cat /storage/input/test_data.txt)"
echo "Execution Time: $(date)"
echo "--------------------------------"

