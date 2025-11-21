import pandas as pd
import os

chunk_size = 200000  # 200K rows per chunk

files = [
    ('data/processed/reviews_filtered.parquet', 'reviews_filtered'),
    ('data/processed/users_filtered.parquet', 'users_filtered'),
    ('data/processed/businesses_filtered.parquet', 'businesses_filtered')
]

os.makedirs('data/chunks', exist_ok=True)

print("Splitting files into chunks...\n")

for file_path, base_name in files:
    print(f"Processing: {base_name}")
    df = pd.read_parquet(file_path)
    total_rows = len(df)
    num_chunks = (total_rows // chunk_size) + 1
    
    print(f"Total rows: {total_rows:,}")
    print(f"Creating {num_chunks} chunks...")
    
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_rows)
        chunk = df.iloc[start_idx:end_idx]
        
        output_file = f"data/chunks/{base_name}_chunk_{i:03d}.parquet"
        chunk.to_parquet(output_file, index=False)
        print(f"  Created: {output_file} ({len(chunk):,} rows)")
    
    print()

print("All files split!")
