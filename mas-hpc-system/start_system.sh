#!/bin/bash
# 1. Clear old logs and reset state
mkdir -p logs
rm -f logs/*.log
echo '{"pending_jobs":0, "active_instances":[], "last_error":"", "ai_fix":""}' > cluster_state.json

# 2. Start all agents in the background
source venv/bin/activate
nohup python3 agent_1_detector.py > /dev/null 2>&1 &
nohup python3 agent_2_scaling.py > /dev/null 2>&1 &
nohup python3 agent_3_diagnostic.py > /dev/null 2>&1 &
nohup python3 agent_4_monitor.py > /dev/null 2>&1 &

# 3. Start the Admin Dashboard
streamlit run admin_dashboard.py --server.port 8501
