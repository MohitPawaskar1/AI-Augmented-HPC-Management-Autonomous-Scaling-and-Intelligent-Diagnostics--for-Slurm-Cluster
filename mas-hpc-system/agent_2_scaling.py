import boto3, subprocess, time, os, json, fcntl

# --- CONFIGURATION (Keep your existing settings) ---
REGION, AMI_ID, INSTANCE_TYPE = "us-east-1", "ami-0e2c8caa4b6378d8c", "t3.micro"
KEY_NAME, SECURITY_GROUP, SUBNET_ID = "slurm-cluster-key", "sg-07bbf21e773894519", "subnet-01ca5e0ad55d5bb1b"
KEY_PATH = "/home/cluster-admin/mas-hpc/slurm-cluster-key.pem"
STATE_FILE, LOG_FILE = "cluster_state.json", "logs/scaler.log"
TS_AUTH_KEY = "tskey-auth-kEkVDMqxTD11CNTRL-CX2H4djWHnat3X2dXbz3naoLJLvkBQbqA" 

ec2 = boto3.client('ec2', region_name=REGION)

def log_event(msg):
    print(f"LOG: {msg}")
    if not os.path.exists("logs"): os.makedirs("logs")
    with open(LOG_FILE, "a") as f: f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {msg}\n")

def get_active_ts_ip(hostname):
    try:
        res = subprocess.check_output(["tailscale", "status", "--json"]).decode()
        data = json.loads(res); peers = data.get("Peer")
        if peers:
            for peer in peers.values():
                if peer.get("HostName", "").split('.')[0] == hostname and peer.get("Online"):
                    return peer.get("TailscaleIPs")[0]
        return None
    except: return None

def launch_aws_node(node_name):
    user_data_script = f"#!/bin/bash\ncurl -fsSL https://tailscale.com/install.sh | sh\n/usr/bin/tailscale up --authkey={TS_AUTH_KEY} --hostname={node_name} --ssh --accept-dns=false --reset --force-reauth"
    log_event(f"Requesting {INSTANCE_TYPE} for {node_name}")
    instance = ec2.run_instances(ImageId=AMI_ID, InstanceType=INSTANCE_TYPE, KeyName=KEY_NAME, MinCount=1, MaxCount=1, SecurityGroupIds=[SECURITY_GROUP], SubnetId=SUBNET_ID, UserData=user_data_script, TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': node_name}]}])
    iid = instance['Instances'][0]['InstanceId']
    ec2.get_waiter('instance_running').wait(InstanceIds=[iid])
    return iid

def main():
    log_event("Agent-2: Scaling service initialized.")
    while True:
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r+") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    
                    # Safe Read - Prevents Char 0 Error
                    content = f.read()
                    if not content:
                        fcntl.flock(f, fcntl.LOCK_UN)
                        time.sleep(1)
                        continue
                    try:
                        state = json.loads(content)
                    except:
                        fcntl.flock(f, fcntl.LOCK_UN)
                        time.sleep(1)
                        continue

                    # Scaling Up
                    if state.get("agent2_request"):
                        req = state["agent2_request"].pop(0)
                        node_count = min(int(req.get('node_count', 1)), 2)
                        for i in range(1, node_count + 1):
                            node_name = f"aws-node{i}"
                            iid = launch_aws_node(node_name)
                            state.setdefault("active_instances", []).append({"id": iid, "node": node_name})
                            ts_ip = None
                            for _ in range(15):
                                ts_ip = get_active_ts_ip(node_name)
                                if ts_ip: break
                                time.sleep(10)
                            if ts_ip:
                                log_event(f"Node {node_name} active at {ts_ip}. Provisioning...")
                                subprocess.run(["ansible-playbook", "-i", f"{ts_ip},", "/home/cluster-admin/mas-hpc/provision_node.yml", "--user", "ubuntu", "--private-key", KEY_PATH, "--ssh-common-args", "-o StrictHostKeyChecking=no"], check=True)
                                subprocess.run(["sudo", "scontrol", "update", f"NodeName={node_name}", "State=DOWN", "Reason=Resetting"])
                                subprocess.run(["sudo", "scontrol", "update", f"NodeName={node_name}", f"NodeAddr={ts_ip}", "State=RESUME"])
                        f.seek(0); f.truncate(); json.dump(state, f, indent=4)

                    # Scaling Down
                    if state.get("scale_down_requested"):
                        # ... (Keep existing termination logic) ...
                        state["scale_down_requested"] = False
                        f.seek(0); f.truncate(); json.dump(state, f, indent=4)
                    
                    fcntl.flock(f, fcntl.LOCK_UN)
            except Exception as e: pass
        time.sleep(5)

if __name__ == "__main__": main()
