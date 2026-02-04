#!/bin/bash
#SBATCH --job-name=logic_fail
#SBATCH --partition=local
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --output=/storage/output/logic_test.out

echo "Starting job with a hidden logic error..."

# This command does not exist and will cause a non-zero exit code
run_complex_simulation_v99 --input=/data/none

if [ $? -ne 0 ]; then
    echo "Simulation failed as expected."
    exit 1
fi
