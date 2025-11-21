import pandas as pd
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
processed_bucket = os.getenv('S3_PROCESSED_BUCKET')

print("=== CLEANING DATA ===\n")

# Download from S3 raw bucket
print("Downloading from S3...")
s3.download_file(raw_bucket, 'reviews_filtered.parquet', 'data/temp_reviews.parquet')
s3.download_file(raw_bucket, 'users_filtered.parquet', 'data/temp_users.parquet')
s3.download_file(raw_bucket, 'businesses_filtered.parquet', 'data/temp_businesses.parquet')

print("\n=== CLEANING REVIEWS ===")
df_reviews = pd.read_parquet('data/temp_reviews.parquet')
print(f"Initial reviews: {len(df_reviews):,}")

# Remove duplicates
df_reviews = df_reviews.drop_duplicates(subset=['review_id'])
print(f"After removing duplicates: {len(df_reviews):,}")

# Remove missing text
df_reviews = df_reviews[df_reviews['text'].notna()]
df_reviews = df_reviews[df_reviews['text'].str.strip() != '']
print(f"After removing missing text: {len(df_reviews):,}")

# Validate star ratings (1-5)
df_reviews = df_reviews[df_reviews['stars'].between(1, 5)]
print(f"After validating stars: {len(df_reviews):,}")

# Save cleaned reviews
df_reviews.to_parquet('data/temp_reviews_clean.parquet', index=False)
print("Cleaned reviews saved\n")

print("=== CLEANING USERS ===")
df_users = pd.read_parquet('data/temp_users.parquet')
print(f"Initial users: {len(df_users):,}")

# Remove invalid records (missing user_id)
df_users = df_users[df_users['user_id'].notna()]
print(f"After removing invalid records: {len(df_users):,}")

df_users.to_parquet('data/temp_users_clean.parquet', index=False)
print("Cleaned users saved\n")

print("=== CLEANING BUSINESSES ===")
df_businesses = pd.read_parquet('data/temp_businesses.parquet')
print(f"Initial businesses: {len(df_businesses):,}")

# Standardize city names (title case)
df_businesses['city'] = df_businesses['city'].str.title().str.strip()
print(f"City names standardized: {len(df_businesses['city'].unique())} unique cities")

df_businesses.to_parquet('data/temp_businesses_clean.parquet', index=False)
print("Cleaned businesses saved\n")

print("=== UPLOADING TO PROCESSED BUCKET ===")
files_to_upload = [
    ('data/temp_reviews_clean.parquet', 'reviews_clean.parquet'),
    ('data/temp_users_clean.parquet', 'users_clean.parquet'),
    ('data/temp_businesses_clean.parquet', 'businesses_clean.parquet')
]

for local_file, s3_key in files_to_upload:
    print(f"Uploading {s3_key}...")
    s3.upload_file(local_file, processed_bucket, s3_key)
    print(f"Uploaded to s3://{processed_bucket}/{s3_key}")

# Cleanup temp files
import os
for local_file, _ in files_to_upload:
    os.remove(local_file)
os.remove('data/temp_reviews.parquet')
os.remove('data/temp_users.parquet')
os.remove('data/temp_businesses.parquet')

print("\nCleaning complete!")
print(f"\nFinal counts:")
print(f"Reviews: {len(df_reviews):,}")
print(f"Users: {len(df_users):,}")
print(f"Businesses: {len(df_businesses):,}")
