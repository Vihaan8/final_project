import boto3
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

processed_bucket = os.getenv('S3_PROCESSED_BUCKET')

print("Deleting ALL files in processed bucket...")

# Delete everything
response = s3.list_objects_v2(Bucket=processed_bucket)
if 'Contents' in response:
    for obj in response['Contents']:
        s3.delete_object(Bucket=processed_bucket, Key=obj['Key'])
        print(f"Deleted: {obj['Key']}")

print("\n✓ Processed bucket cleaned")
