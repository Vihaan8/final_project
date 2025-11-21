import json
import boto3
import pandas as pd
from io import BytesIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    raw_bucket = event['raw_bucket']
    processed_bucket = event['processed_bucket']
    chunk_key = event['chunk_key']
    
    print(f"Processing: {chunk_key}")
    
    # Download chunk
    obj = s3.get_object(Bucket=raw_bucket, Key=chunk_key)
    df = pd.read_parquet(BytesIO(obj['Body'].read()))
    
    print(f"Loaded {len(df)} rows")
    
    # Clean based on file type
    if 'review' in chunk_key:
        df = df.drop_duplicates(subset=['review_id'])
        df = df[df['text'].notna()]
        df = df[df['text'].str.strip() != '']
        df = df[df['stars'].between(1, 5)]
    elif 'user' in chunk_key:
        df = df[df['user_id'].notna()]
    elif 'business' in chunk_key:
        df['city'] = df['city'].str.title().str.strip()
    
    print(f"Cleaned to {len(df)} rows")
    
    # Upload to processed bucket
    output_key = chunk_key.replace('chunks/', 'processed_chunks/').replace('filtered', 'clean')
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    
    s3.put_object(
        Bucket=processed_bucket,
        Key=output_key,
        Body=buffer.getvalue()
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {len(df)} rows')
    }
