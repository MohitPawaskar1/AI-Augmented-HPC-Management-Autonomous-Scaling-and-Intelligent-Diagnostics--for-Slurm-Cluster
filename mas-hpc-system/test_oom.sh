#!/bin/bash
#SBATCH --job-name=OOM_Test
#SBATCH --partition=cloud
#SBATCH --mem=10M               # Extremely low memory limit
#SBATCH --output=/storage/output/oom_test_%j.out
#SBATCH --error=/storage/output/oom_test_%j.err

echo "Starting memory allocation..."
# This Python command attempts to allocate roughly 800MB of RAM
python3 -c "import numpy as np; a = np.ones((10000, 10000))"
