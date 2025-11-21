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

print(f"Uploading chunks to s3://{raw_bucket}/chunks/\n")

chunk_files = [f for f in os.listdir('data/chunks') if f.endswith('.parquet')]

for chunk_file in tqdm(chunk_files, desc="Uploading"):
    local_path = f"data/chunks/{chunk_file}"
    s3_key = f"chunks/{chunk_file}"
    s3.upload_file(local_path, raw_bucket, s3_key)

print(f"\nUploaded {len(chunk_files)} chunks!")
