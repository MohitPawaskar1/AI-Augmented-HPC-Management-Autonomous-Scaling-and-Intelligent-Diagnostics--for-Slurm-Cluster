#!/bin/bash
#SBATCH --job-name=DEEP_DIAGNOSTIC
#SBATCH --partition=local
#SBATCH --output=slurm-%j.out

set -e  # <--- CRITICAL: Exit on any error

echo "🚀 Starting Deep Analysis Test..."

# Trigger a ModuleNotFoundError (Python exits with code 1)
python3 -c "import non_existent_library"

echo "This line should never be reached."
