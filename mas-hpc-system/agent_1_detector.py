import subprocess
import time
import json
import os
import fcntl
from datetime import datetime
from cluster_config import SYSTEM_SETTINGS, LOCAL_NODE_SPECS, CLUSTER_LOGIC, SLURM_STATES

processed_jobs = set()

def get_job_specs(job_id):
    try:
        cmd = f"scontrol show job {job_id} -o"
        output = subprocess.check_output(cmd, shell=True).decode()
        cpus = 0
        mem_gb = 0
        if "NumCPUs=" in output:
            cpus = int(output.split("NumCPUs=")[1].split()[0])
        if "Mem=" in output:
            raw_mem = output.split("Mem=")[1].split()[0]
            val = int(''.join(filter(str.isdigit, raw_mem)))
            mem_gb = val / 1024 if 'M' in raw_mem.upper() else val
        return cpus, mem_gb
    except: return 0, 0

def save_event(event_type, data):
    try:
        with open(SYSTEM_SETTINGS["STATE_FILE"], 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX) # Wait for exclusive access
            try:
                state = json.load(f)
            except:
                state = {"agent2_request": [], "agent3_request": [], "active_instances": [], "scale_down_requested": False}
            
            state.setdefault(event_type, []).append(data)
            f.seek(0)
            f.truncate()
            json.dump(state, f, indent=4)
            f.flush()
            fcntl.flock(f, fcntl.LOCK_UN)
    except Exception as e: 
        print(f"State Save Error: {e}")

def get_queue_data():
    try:
        cmd_squeue = 'squeue -h --format="%i,%t,%D,%R"'
        active = subprocess.check_output(cmd_squeue, shell=True).decode().splitlines()
        cmd_sacct = 'sacct -n -X --format="JobID,State" --starttime=$(date -d "2 minutes ago" +%H:%M:%S)'
        finished_raw = subprocess.check_output(cmd_sacct, shell=True).decode().splitlines()
        results = [line.strip() for line in active]
        for l in finished_raw:
            parts = l.split()
            if len(parts) >= 2 and any(s in parts[1] for s in SLURM_STATES["DIAGNOSTIC"]):
                results.append(f"{parts[0]},{parts[1]},0,None")
        return results
    except: return []

def main():
    print("Agent-1: High-Frequency Detector Active...")
    while True:
        try:
            lines = get_queue_data()
            for line in lines:
                parts = line.split(',')
                if len(parts) < 2: continue
                jid, status, nodes, reason = [c.strip() for c in parts]

                if jid in processed_jobs: continue

                # 1. Failure Detection
                if any(s in status for s in SLURM_STATES["DIAGNOSTIC"]):
                    if status == 'NODE_FAIL' and "aws-node" in line: continue
                    print(f"Agent-1: Job {jid} failure detected ({status})")
                    save_event("agent3_request", {"job_id": jid, "status": status})
                    processed_jobs.add(jid)

                # 2. Pending Logic
                elif status == 'PD':
                    if "JobHeld" in reason:
                        save_event("agent3_request", {"job_id": jid, "status": "HELD"})
                        processed_jobs.add(jid)
                        continue

                    req_cpu, req_mem = get_job_specs(jid)
                    if req_cpu > LOCAL_NODE_SPECS["CPU_PER_NODE"] or req_mem > LOCAL_NODE_SPECS["MEM_PER_NODE_GB"]:
                        save_event("agent3_request", {"job_id": jid, "status": "HARDWARE_LIMIT_EXCEEDED", "req_cpu": req_cpu, "req_mem": req_mem})
                        processed_jobs.add(jid)
                        continue
                    
                    if int(nodes) > LOCAL_NODE_SPECS["MAX_LOCAL_NODES"] or "Resources" in reason:
                        # RESTORED Y/N PROMPT
                        auth = input(f"\nAgent-1: Job {jid} requires Cloud Burst. Authorize AWS Provisioning? (y/n): ")
                        if auth.lower() == 'y':
                            save_event("agent2_request", {"job_id": jid, "node_count": int(nodes)})
                        processed_jobs.add(jid)

        except: pass
        time.sleep(5)

if __name__ == "__main__": main()
