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

print("Removing old chunks...")

# List all chunks
response = s3.list_objects_v2(Bucket=raw_bucket, Prefix='chunks/')
if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        # Keep only reviews_chunk files, delete old business/user chunks
        if 'reviews_chunk' not in key:
            s3.delete_object(Bucket=raw_bucket, Key=key)
            print(f"Deleted: {key}")
        else:
            print(f"Kept: {key}")

print("\n✓ Cleanup complete")
