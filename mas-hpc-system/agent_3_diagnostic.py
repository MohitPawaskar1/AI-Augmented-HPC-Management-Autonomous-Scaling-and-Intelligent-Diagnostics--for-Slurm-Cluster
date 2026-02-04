import json, time, os, fcntl, random, subprocess
from google import genai
from cluster_config import SYSTEM_SETTINGS, LOCAL_NODE_SPECS

client = genai.Client(api_key=SYSTEM_SETTINGS["GEMINI_API_KEY"])

def get_job_logs(job_id):
    try:
        # Ask Slurm exactly where the log is
        cmd = f"scontrol show job {job_id} | grep -E 'StdOut=|StdErr=' | cut -d'=' -f2"
        slurm_paths = subprocess.check_output(cmd, shell=True).decode().split()
    except: slurm_paths = []

    search_paths = list(set(slurm_paths + [f"slurm-{job_id}.out", f"/storage/output/dir.err", f"/storage/output/syntax.err"]))
    
    for attempt in range(5):
        for path in search_paths:
            if os.path.exists(path) and os.path.getsize(path) > 0:
                try:
                    with open(path, "r") as f: return f.read()[-2000:]
                except: pass
        time.sleep(5)
    return None

def analyze_failure(req):
    jid, status = req['job_id'], req.get('status', 'FAILED')
    if status == "HARDWARE_LIMIT_EXCEEDED":
        cpu, mem = req.get('req_cpu'), req.get('req_mem')
        return jid, f"ERROR: Resource Configuration Error\nWHY: Requested {cpu} CPU exceeds node limit.\nFIX: Reduce SBATCH resources."
    if status == "HELD":
        return jid, f"ERROR: Job Execution Blocked\nWHY: User or Admin hold placed on job.\nFIX: Run 'scontrol release {jid}'."

    logs = get_job_logs(jid)
    if not logs: return jid, "ERROR: Log Sync Failure\nWHY: Logs not found in NFS share.\nFIX: Check /storage/output mount."

    prompt = f"Analyze Slurm Job {jid} failure log. Format: ERROR, WHY, FIX (3 lines).\nLOG:\n{logs}"
    try:
        res = client.models.generate_content(model='gemini-2.0-flash', contents=prompt, config={'temperature': 0.1})
        return jid, res.text.strip()
    except: return jid, "ERROR: AI Timeout\nWHY: API Busy."

def main():
    print("Agent-3: Diagnostic Engine Active")
    while True:
        with open(SYSTEM_SETTINGS["STATE_FILE"], "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                state = json.load(f)
                queue = state.get("agent3_request", [])
                if queue:
                    current_batch = list(queue)
                    state["agent3_request"] = []
                    f.seek(0); f.truncate(); json.dump(state, f, indent=4)
                    fcntl.flock(f, fcntl.LOCK_UN)
                    for req in current_batch:
                        jid, report = analyze_failure(req)
                        print(f"\n[REPORT JOB {jid}]\n{report}\n{'-'*30}")
                else: fcntl.flock(f, fcntl.LOCK_UN)
            except: fcntl.flock(f, fcntl.LOCK_UN)
        time.sleep(5)

if __name__ == "__main__": main()
