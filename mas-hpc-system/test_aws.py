import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2', region_name='us-east-1')

def dry_run_test():
    try:
        # DryRun=True means it checks permissions but DOES NOT start a real machine
        ec2.run_instances(
            ImageId='ami-0e2c8caa4b6378d8c', # Default Ubuntu 24.04 in us-east-1
            InstanceType='t3.medium',
            MaxCount=1,
            MinCount=1,
            DryRun=True
        )
    except ClientError as e:
        if 'DryRunOperation' in str(e):
            print("✅ SUCCESS: Your AWS credentials and network can reach the API!")
        else:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    dry_run_test()
