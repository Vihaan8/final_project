import boto3
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

raw_bucket = os.getenv('S3_RAW_BUCKET')
processed_bucket = os.getenv('S3_PROCESSED_BUCKET')

print("Creating S3 buckets...")

for bucket in [raw_bucket, processed_bucket]:
    try:
        s3.create_bucket(Bucket=bucket)
        print(f"Created: {bucket}")
    except Exception as e:
        print(f"{bucket}: {e}")

print("\nBuckets ready!")
