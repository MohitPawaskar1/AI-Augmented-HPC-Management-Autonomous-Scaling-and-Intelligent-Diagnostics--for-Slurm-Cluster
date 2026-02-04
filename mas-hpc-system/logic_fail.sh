#!/bin/bash
#SBATCH --job-name=logic_fail
#SBATCH --partition=local
#SBATCH --nodes=1
#SBATCH --output=/storage/output/logic_test.out

set -e  # <--- THIS IS THE KEY: Exit immediately if a command fails

# This will now trigger an immediate job failure
non_existent_command_v100

echo "This line will never be reached"
