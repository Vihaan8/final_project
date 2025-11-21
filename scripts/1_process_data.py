"""
Process raw Yelp data:
1. Filter users with 20+ reviews
2. Keep only their reviews
3. Keep only businesses in top cities
4. Save as Parquet (smaller, faster)
"""
import pandas as pd
import json
from tqdm import tqdm

print("=== STEP 1: Load and Filter Users ===")
print("Reading users in chunks...")

# Read ALL users, filter to 20+ reviews
users = []
with open('data/raw/yelp_academic_dataset_user.json', 'r') as f:
    for line in tqdm(f, desc="Loading users"):
        user = json.loads(line)
        if user['review_count'] >= 20:
            users.append(user)

df_users = pd.DataFrame(users)
print(f"Kept {len(df_users):,} users with 20+ reviews")

# Save filtered users
df_users.to_parquet('data/processed/users_filtered.parquet', index=False)
print("Saved to data/processed/users_filtered.parquet\n")

# Get user IDs for filtering reviews
qualified_user_ids = set(df_users['user_id'])

print("=== STEP 2: Filter Reviews ===")
print("Reading reviews in chunks...")

# Process reviews in chunks (memory efficient)
chunk_size = 100000
reviews_filtered = []

with open('data/raw/yelp_academic_dataset_review.json', 'r') as f:
    chunk = []
    for line in tqdm(f, desc="Processing reviews"):
        review = json.loads(line)
        
        if review['user_id'] in qualified_user_ids:
            chunk.append(review)
        
        if len(chunk) >= chunk_size:
            df_chunk = pd.DataFrame(chunk)
            reviews_filtered.append(df_chunk)
            chunk = []
    
    if chunk:
        df_chunk = pd.DataFrame(chunk)
        reviews_filtered.append(df_chunk)

df_reviews = pd.concat(reviews_filtered, ignore_index=True)
print(f"Kept {len(df_reviews):,} reviews from qualified users")

df_reviews.to_parquet('data/processed/reviews_filtered.parquet', index=False)
print("Saved to data/processed/reviews_filtered.parquet\n")

print("=== STEP 3: Filter Businesses ===")

business_ids_needed = set(df_reviews['business_id'])

businesses = []
with open('data/raw/yelp_academic_dataset_business.json', 'r') as f:
    for line in tqdm(f, desc="Loading businesses"):
        business = json.loads(line)
        if business['business_id'] in business_ids_needed:
            businesses.append(business)

df_businesses = pd.DataFrame(businesses)
print(f"Kept {len(df_businesses):,} businesses")

df_businesses.to_parquet('data/processed/businesses_filtered.parquet', index=False)
print("Saved to data/processed/businesses_filtered.parquet\n")

print("=== SUMMARY ===")
print(f"Users: {len(df_users):,}")
print(f"Reviews: {len(df_reviews):,}")
print(f"Businesses: {len(df_businesses):,}")
print("\nFiltered data ready in data/processed/")
