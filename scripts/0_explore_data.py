import pandas as pd
import json

def explore_yelp_data():
    print("=== EXPLORING YELP DATA ===\n")
    
    # Reviews
    print("Loading reviews (first 1000)...")
    reviews = []
    with open('data/raw/yelp_academic_dataset_review.json', 'r') as f:
        for i, line in enumerate(f):
            if i >= 1000:
                break
            reviews.append(json.loads(line))
    
    df_reviews = pd.DataFrame(reviews)
    print(f"Review columns: {df_reviews.columns.tolist()}")
    print(f"Sample:\n{df_reviews[['user_id', 'business_id', 'stars', 'text']].head(3)}\n")
    
    # Businesses
    print("Loading businesses (first 1000)...")
    businesses = []
    with open('data/raw/yelp_academic_dataset_business.json', 'r') as f:
        for i, line in enumerate(f):
            if i >= 1000:
                break
            businesses.append(json.loads(line))
    
    df_businesses = pd.DataFrame(businesses)
    print(f"Business columns: {df_businesses.columns.tolist()}")
    print(f"\nTop cities:\n{df_businesses['city'].value_counts().head(10)}\n")
    
    # Users
    print("Loading users (first 1000)...")
    users = []
    with open('data/raw/yelp_academic_dataset_user.json', 'r') as f:
        for i, line in enumerate(f):
            if i >= 1000:
                break
            users.append(json.loads(line))
    
    df_users = pd.DataFrame(users)
    print(f"User columns: {df_users.columns.tolist()}")
    print(f"\nReview count stats:\n{df_users['review_count'].describe()}")
    print(f"\nUsers with 20+ reviews: {len(df_users[df_users['review_count'] >= 20])}")

if __name__ == "__main__":
    explore_yelp_data()
