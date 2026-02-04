#!/bin/bash
# MAS-HPC Final Demo Suite - Centralized NFS Logging
echo "🚀 Submitting 10 Scenarios for Agent-1 and Agent-3..."

OUT_DIR="/storage/output"
mkdir -p $OUT_DIR

# 1. Cloud Burst (Forces PD -> CF -> R transition)
sbatch -p cloud -N 1 --job-name="BURST" -o $OUT_DIR/burst.out -e $OUT_DIR/burst.err --wrap="hostname; sleep 20"

# 2. Hardware Overlimit (Trigger Agent-1 Pre-screen)
sbatch --cpus-per-task=17 --overcommit --job-name="HW_ERR" -o $OUT_DIR/hw.out -e $OUT_DIR/hw.err --wrap="sleep 5"

# 3. Python Syntax Error
echo -e "#!/bin/bash\nexport PYTHONUNBUFFERED=1\npython3 -c 'print(\"Hi\"'" > syntax.slurm
sbatch --job-name="SYNTAX" -o $OUT_DIR/syntax.out -e $OUT_DIR/syntax.err syntax.slurm

# 4. Zero Division
sbatch --job-name="MATH_ERR" -o $OUT_DIR/math.out -e $OUT_DIR/math.err --wrap="python3 -c '1/0'"

# 5. OOM (Memory Exhaustion)
sbatch --mem=1M --job-name="MEM_ERR" -o $OUT_DIR/mem.out -e $OUT_DIR/mem.err --wrap="python3 -c 'a=[1]*10**8'"

# 6. Invalid Command
sbatch --job-name="CMD_ERR" -o $OUT_DIR/cmd.out -e $OUT_DIR/cmd.err --wrap="unknown_command_v99"

# 7. Time Limit Violation
sbatch --time=00:00:05 --job-name="TIME_ERR" -o $OUT_DIR/time.out -e $OUT_DIR/time.err --wrap="sleep 30"

# 8. Admin Hold (Detected as PD - JobHeldUser)
jid=$(sbatch --parsable --job-name="HELD_ERR" -o $OUT_DIR/held.out -e $OUT_DIR/held.err --wrap="echo hi")
scontrol hold $jid

# 9. Directory Access Error
sbatch --job-name="DIR_ERR" -o $OUT_DIR/dir.out -e $OUT_DIR/dir.err --wrap="cd /root/forbidden_data"

# 10. Permission Error
sbatch --job-name="PERM_ERR" -o $OUT_DIR/perm.out -e $OUT_DIR/perm.err --wrap="cat /etc/shadow"

echo "10 Jobs Submitted. Logs are centralizing in $OUT_DIR"
