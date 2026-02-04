#!/bin/bash
#SBATCH --job-name=CLOUD_LOOP
#SBATCH --partition=cloud          
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --output=/storage/output/cloud_loop_%j.out

echo "🚀 Deployment started on: $(hostname)"
echo "Cluster State: Active"

# Correct Bash Loop Syntax
for i in {1..100}
do
    echo "Processing iteration: $i"
    sleep 1
done

echo "✅ Cloud loop finished successfully."
