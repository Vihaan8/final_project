-- Add tags column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS tags JSONB;

-- Create GIN index for fast JSON queries
CREATE INDEX IF NOT EXISTS idx_users_tags ON users USING GIN (tags);

-- Verify
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'users' AND column_name = 'tags';
