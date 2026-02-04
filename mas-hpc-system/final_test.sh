#!/bin/bash
echo "🚀 Launching Modular Agent V20 Test Suite (10 Scenarios)..."

# --------- OUTPUT DIRECTORY ----------
LOG_DIR="/home/acts/project/slurm_ai_agent/logs"
mkdir -p $LOG_DIR

# 1. HIGH NODE REQUEST (Triggers cloud burst)
cat > job1_high_nodes.slurm <<EOF
#!/bin/bash
#SBATCH --nodes=6
#SBATCH --time=00:01:00
echo "Running high node job"
EOF
echo "[1/10] High Node Request (6 Nodes)..."
sbatch job1_high_nodes.slurm

# 2. NORMAL JOB (should run clean)
cat > job2_normal.slurm <<EOF
#!/bin/bash
#SBATCH --nodes=1
echo "Normal job running fine"
EOF
echo "[2/10] Normal Request..."
sbatch job2_normal.slurm

# 3. MEMORY EXHAUSTION
cat > job3_mem.slurm <<EOF
#!/bin/bash
#SBATCH --mem=10M
python3 - << 'EOPY'
a = 'x' * (1024*1024*200)
print(len(a))
EOPY
EOF
echo "[3/10] Memory Exhaustion..."
sbatch job3_mem.slurm

# 4. TIME LIMIT VIOLATION
cat > job4_time.slurm <<EOF
#!/bin/bash
#SBATCH --time=00:00:02
sleep 10
EOF
echo "[4/10] Time Limit Violation..."
sbatch job4_time.slurm

# 5. ADMIN HOLD
cat > job5_hold.slurm <<EOF
#!/bin/bash
#SBATCH --nodes=1
echo "Held job"
EOF
jid=$(sbatch job5_hold.slurm | awk '{print $4}')
echo "[5/10] Admin Hold..."
scontrol hold $jid

# 6. SUSPENDED JOB
cat > job6_suspend.slurm <<EOF
#!/bin/bash
#SBATCH --nodes=1
sleep 100
EOF
jid6=$(sbatch job6_suspend.slurm | awk '{print $4}')
echo "[6/10] Suspended State..."
sleep 2
scontrol suspend $jid6

# 7. PYTHON SYNTAX ERROR
cat > job7_pyerror.slurm <<EOF
#!/bin/bash
python3 - << 'EOPY'
print("Hello"
EOPY
EOF
echo "[7/10] Python Syntax Bug..."
sbatch job7_pyerror.slurm

# 8. INVALID COMMAND
cat > job8_invalidcmd.slurm <<EOF
#!/bin/bash
notacommand123
EOF
echo "[8/10] Invalid Command..."
sbatch job8_invalidcmd.slurm

# 9. INVALID CONSTRAINT / FEATURE
cat > job9_badconstraint.slurm <<EOF
#!/bin/bash
#SBATCH --constraint=fakegpu
echo "Invalid constraint job"
EOF
echo "[9/10] Invalid Constraint..."
sbatch job9_badconstraint.slurm

# 10. SUCCESS FAST
cat > job10_fast.slurm <<EOF
#!/bin/bash
echo "Fast job done"
EOF
echo "[10/10] Fast Completion..."
sbatch job10_fast.slurm

echo
echo "✅ All 10 test scenarios submitted."
echo "👉 Switch to your agent terminal to see analysis."

