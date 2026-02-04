#!/bin/bash
#SBATCH --job-name=cloud_test
#SBATCH --partition=cloud
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=/storage/output/cloud_burst_success.out
#SBATCH --error=/storage/output/cloud_burst_error.err

echo "Job started on: $(hostname)"
echo "Tailscale IP: $(tailscale ip -4)"
echo "Storage Check: $(ls /storage/output)"

# Simulation of work
for i in {1..10}; do
    echo "Processing step $i on cloud hardware..."
    sleep 5
done

echo "Cloud burst job completed successfully."
