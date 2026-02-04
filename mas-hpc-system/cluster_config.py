import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_SETTINGS = {
    "STATE_FILE": "/home/cluster-admin/mas-hpc/cluster_state.json",
    "LOG_DIR": "logs/",
    "POLL_INTERVAL": 10,
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY")
}

LOCAL_NODE_SPECS = {
    "CPU_PER_NODE": 16,
    "MEM_PER_NODE_GB": 40,
    "MAX_LOCAL_NODES": 3,
    "PARTITION": "local"
}

CLUSTER_LOGIC = {
    "URGENCY_THRESHOLD": 120, 
    "STORAGE_PATHS": ["/storage/input", "/storage/output"]
}

CLOUD_PROVISIONING = {
    "REGION": "us-east-1",
    "AMI_ID": "ami-0e2c8caa4b6378d8c",
    "INSTANCE_TYPE": "t3.micro",
    "VCPU_LIMIT": 16,
    "MAX_BURST_NODES": 2,
    "TS_AUTH_KEY": os.getenv("TS_AUTH_KEY", "tskey-auth-kEkVDMqxTD11CNTRL-CX2H4djWHnat3X2dXbz3naoLJLvkBQbqA")
}

SLURM_STATES = {
    "DIAGNOSTIC": ['FAILED', 'TIMEOUT', 'NODE_FAIL', 'CANCELLED', 'CA', 'OUT_OF_MEMORY', 'SUSPENDED'],
    "PENDING": ['PD', 'CF']
}
