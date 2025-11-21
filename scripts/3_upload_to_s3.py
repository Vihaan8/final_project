import boto3
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

raw_bucket = os.getenv('S3_RAW_BUCKET')

files = [
    'data/processed/users_filtered.parquet',
    'data/processed/reviews_filtered.parquet',
    'data/processed/businesses_filtered.parquet'
]

print(f"Uploading to s3://{raw_bucket}/\n")

for file_path in files:
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path) / (1024**3)
    
    print(f"Uploading {file_name} ({file_size:.2f} GB)...")
    
    s3.upload_file(file_path, raw_bucket, file_name)
    print(f"Uploaded: s3://{raw_bucket}/{file_name}\n")

print("All files uploaded successfully!")
