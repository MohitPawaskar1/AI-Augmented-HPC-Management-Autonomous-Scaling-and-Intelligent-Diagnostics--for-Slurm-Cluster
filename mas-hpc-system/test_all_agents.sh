#!/bin/bash
#SBATCH --job-name=agent_triathlon
#SBATCH --nodes=4                # Forces PD state (3 local + 1 cloud)
#SBATCH --partition=cloud,local  # Allows using both partitions
#SBATCH --output=agent_test_%j.log
#SBATCH --error=agent_test_%j.err

echo "🚀 Job started on $(hostname) at $(date)"

# Simulate a heavy calculation
sleep 10

# --- THE TRIGGER ---
echo "❌ Simulating a critical failure for Agent-3 to analyze..."
# This command doesn't exist, which will cause a 'command not found' error
/usr/bin/simulate_crash_and_burn_v1

# Exit with an error code to ensure Slurm marks it as FAILED
exit 1
