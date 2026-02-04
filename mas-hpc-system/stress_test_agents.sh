#!/bin/bash

# 1. Resource Shortage (Triggers Agent-1 Cloud Burst prompt)
echo "Submitting Scenario 1: Resource Shortage..."
sbatch -N 5 --job-name="TEST_SHORTAGE" --wrap "sleep 60"

# 2. Permission Denied (Triggers Agent-3: File access)
echo "Submitting Scenario 2: Permission Denied..."
sbatch --job-name="TEST_PERM" --wrap "ls /root/secrets"

# 3. Python Syntax Error (Triggers Agent-3: Code Analysis)
echo "Submitting Scenario 3: Python Syntax..."
sbatch --job-name="TEST_SYNTAX" --wrap "python3 -c 'print(\"Missing bracket' "

# 4. Out of Memory (Simulated via tiny allocation)
echo "Submitting Scenario 4: OOM Simulation..."
sbatch --mem=1M --job-name="TEST_OOM" --wrap "python3 -c 'a=[1]*10**8'"

# 5. Invalid Command (Triggers Agent-3: Typo Detection)
echo "Submitting Scenario 5: Typo Command..."
sbatch --job-name="TEST_TYPO" --wrap "gtit status"

# 6. Zero Division Error (Triggers Agent-3: Logic Analysis)
echo "Submitting Scenario 6: Zero Division..."
sbatch --job-name="TEST_MATH" --wrap "python3 -c 'x=1/0'"

# 7. Missing Module (Triggers Agent-3: Environment Fix)
echo "Submitting Scenario 7: Missing Module..."
sbatch --job-name="TEST_IMPORT" --wrap "python3 -c 'import non_existent_library'"

# 8. Timeout (Triggers Agent-1: State TO)
echo "Submitting Scenario 8: Timeout..."
sbatch --time=00:00:10 --job-name="TEST_TIMEOUT" --wrap "sleep 30"

# 9. Directory Not Found (Triggers Agent-3: Path Analysis)
echo "Submitting Scenario 9: Missing Dir..."
sbatch --job-name="TEST_DIR" --wrap "cd /non/existent/path"

# 10. Library Mismatch (Triggers Agent-3: Versioning)
echo "Submitting Scenario 10: Shared Library Error..."
sbatch --job-name="TEST_LIB" --wrap "ldconfig -p | grep missing_lib_fake"

echo "------------------------------------------------"
echo "All 10 test scenarios submitted. Check squeue!"
