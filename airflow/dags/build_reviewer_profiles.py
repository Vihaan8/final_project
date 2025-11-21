from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import boto3
import pandas as pd
from io import BytesIO
from collections import Counter
import json
import os

def download_clean_data():
    s3 = boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    
    bucket = os.getenv('S3_PROCESSED_BUCKET')
    print(f"Downloading from bucket: {bucket}")
    
    obj = s3.get_object(Bucket=bucket, Key='users_clean.parquet')
    df_users = pd.read_parquet(BytesIO(obj['Body'].read()))
    df_users.to_parquet('/tmp/users_clean.parquet')
    
    obj = s3.get_object(Bucket=bucket, Key='reviews_clean.parquet')
    df_reviews = pd.read_parquet(BytesIO(obj['Body'].read()))
    df_reviews.to_parquet('/tmp/reviews_clean.parquet')
    
    print(f"Downloaded {len(df_users)} users and {len(df_reviews)} reviews")

def build_profiles():
    df_users = pd.read_parquet('/tmp/users_clean.parquet')
    df_reviews = pd.read_parquet('/tmp/reviews_clean.parquet')
    
    print("Building reviewer profiles...")
    profiles = []
    
    for user_id in df_users['user_id'][:1000]:
        user_reviews = df_reviews[df_reviews['user_id'] == user_id]
        if len(user_reviews) == 0:
            continue
        
        avg_rating = user_reviews['stars'].mean()
        total_reviews = len(user_reviews)
        avg_review_length = user_reviews['text'].str.len().mean()
        
        all_text = ' '.join(user_reviews['text'].str.lower())
        words = [w for w in all_text.split() if len(w) > 4]
        top_words = dict(Counter(words).most_common(10))
        
        rating_tendency = 'harsh' if avg_rating < 3.5 else 'generous' if avg_rating > 4.5 else 'balanced'
        
        profiles.append({
            'user_id': user_id,
            'avg_rating': round(avg_rating, 2),
            'total_reviews': total_reviews,
            'avg_review_length': int(avg_review_length),
            'top_words': json.dumps(top_words),
            'rating_tendency': rating_tendency
        })
    
    df_profiles = pd.DataFrame(profiles)
    df_profiles.to_parquet('/tmp/reviewer_profiles.parquet', index=False)
    print(f"Built {len(df_profiles)} profiles")

def upload_profiles():
    s3 = boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    
    bucket = os.getenv('S3_PROCESSED_BUCKET')
    s3.upload_file('/tmp/reviewer_profiles.parquet', bucket, 'analytics/reviewer_profiles.parquet')
    print("Uploaded to S3!")

with DAG(
    'build_reviewer_profiles',
    description='Build reviewer profiles',
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:
    
    download = PythonOperator(task_id='download_clean_data', python_callable=download_clean_data)
    build = PythonOperator(task_id='build_profiles', python_callable=build_profiles)
    upload = PythonOperator(task_id='upload_profiles', python_callable=upload_profiles)
    
    download >> build >> upload
