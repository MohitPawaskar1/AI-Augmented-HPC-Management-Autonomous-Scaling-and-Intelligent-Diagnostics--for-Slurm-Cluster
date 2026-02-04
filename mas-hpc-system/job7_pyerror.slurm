#!/bin/bash
#SBATCH --job-name=py_error
#SBATCH --partition=local
#SBATCH --nodes=1

# 1. Force exit on ANY error
set -e

# 2. Force Python to flush errors to the log file IMMEDIATELY
export PYTHONUNBUFFERED=1

echo "Starting Python check..."

python3 - << 'EOPY'
print("Hello"
EOPY

echo "This will not print because of set -e"
