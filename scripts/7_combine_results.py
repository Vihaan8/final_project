import boto3
import pandas as pd
from dotenv import load_dotenv
import os
from io import BytesIO
from tqdm import tqdm

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

processed_bucket = os.getenv('S3_PROCESSED_BUCKET')

print("Combining processed chunks...\n")

# List all processed chunks
response = s3.list_objects_v2(Bucket=processed_bucket, Prefix='processed_chunks/')
chunks = [obj['Key'] for obj in response.get('Contents', [])]

print(f"Found {len(chunks)} processed chunks")

# Group by file type
file_types = {'reviews': [], 'users': [], 'businesses': []}

for chunk_key in chunks:
    if 'reviews' in chunk_key:
        file_types['reviews'].append(chunk_key)
    elif 'users' in chunk_key:
        file_types['users'].append(chunk_key)
    elif 'businesses' in chunk_key:
        file_types['businesses'].append(chunk_key)

# Combine each type
for file_type, chunk_list in file_types.items():
    if not chunk_list:
        continue
    
    print(f"\nCombining {len(chunk_list)} {file_type} chunks...")
    
    dfs = []
    for chunk_key in tqdm(chunk_list, desc=f"Loading {file_type}"):
        obj = s3.get_object(Bucket=processed_bucket, Key=chunk_key)
        df = pd.read_parquet(BytesIO(obj['Body'].read()))
        dfs.append(df)
    
    df_combined = pd.concat(dfs, ignore_index=True)
    print(f"Combined into {len(df_combined):,} rows")
    
    # Upload combined file
    output_key = f"{file_type}_clean.parquet"
    buffer = BytesIO()
    df_combined.to_parquet(buffer, index=False)
    buffer.seek(0)
    
    s3.put_object(
        Bucket=processed_bucket,
        Key=output_key,
        Body=buffer.getvalue()
    )
    print(f"Uploaded: s3://{processed_bucket}/{output_key}")

print("\n=== CLEANING COMPLETE ===")
print("Cleaned data in processed bucket!")
