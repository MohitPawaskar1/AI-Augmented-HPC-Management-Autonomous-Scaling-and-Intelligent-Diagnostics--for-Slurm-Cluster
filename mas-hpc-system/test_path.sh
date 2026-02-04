#!/bin/bash
#SBATCH --job-name=Path_Test
#SBATCH --partition=cloud
#SBATCH --output=/non_existent_folder/path_test_%j.out
#SBATCH --error=/non_existent_folder/path_test_%j.err

echo "This job will fail because the output directory doesn't exist."
