import subprocess, time, json, os, fcntl
from cluster_config import SYSTEM_SETTINGS

def get_active_job_count():
    try:
        cmd = "squeue -h -t R,PD,CF,CG"
        out = subprocess.check_output(cmd, shell=True).decode().strip()
        return len(out.splitlines()) if out else 0
    except: return 0

def main():
    print("Agent-4: Resource Monitor Active")
    idle_counter = 0
    while True:
        count = get_active_job_count()
        if count > 0: idle_counter = 0
        else:
            idle_counter += 1
            if idle_counter >= 4:
                with open(SYSTEM_SETTINGS["STATE_FILE"], "r+") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    try:
                        state = json.load(f)
                        if state.get("active_instances"):
                            print("Scale-down requested.")
                            state["scale_down_requested"] = True
                            f.seek(0); f.truncate(); json.dump(state, f, indent=4)
                    except: pass
                    fcntl.flock(f, fcntl.LOCK_UN)
                idle_counter = 0
        time.sleep(30)

if __name__ == "__main__": main()
