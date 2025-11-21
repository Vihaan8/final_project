-- Clean Data Tables (loaded from S3)
CREATE TABLE businesses (
    business_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(10),
    postal_code VARCHAR(20),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    stars DECIMAL(2, 1),
    review_count INTEGER,
    categories TEXT
);

CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    review_count INTEGER,
    yelping_since DATE,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    elite TEXT,
    friends TEXT,
    fans INTEGER,
    average_stars DECIMAL(3, 2),
    compliment_hot INTEGER,
    compliment_more INTEGER,
    compliment_profile INTEGER,
    compliment_cute INTEGER,
    compliment_list INTEGER,
    compliment_note INTEGER,
    compliment_plain INTEGER,
    compliment_cool INTEGER,
    compliment_funny INTEGER,
    compliment_writer INTEGER,
    compliment_photos INTEGER
);

CREATE TABLE reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    business_id VARCHAR(50) REFERENCES businesses(business_id),
    stars INTEGER,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    text TEXT,
    date TIMESTAMP
);

CREATE TABLE reviewer_profiles (
    user_id VARCHAR(50) PRIMARY KEY REFERENCES users(user_id),
    avg_rating DECIMAL(3, 2),
    total_reviews INTEGER,
    avg_review_length INTEGER,
    top_words JSONB,
    rating_tendency VARCHAR(20),
    cities_reviewed TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE city_stats (
    city VARCHAR(100) PRIMARY KEY,
    total_reviews INTEGER,
    avg_rating DECIMAL(3, 2),
    total_businesses INTEGER,
    top_cuisines JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE quiz_responses (
    response_id SERIAL PRIMARY KEY,
    display_name VARCHAR(50),
    city VARCHAR(100),
    quiz_answers JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE taste_twins (
    id SERIAL PRIMARY KEY,
    response_id INTEGER REFERENCES quiz_responses(response_id),
    twin_user_id VARCHAR(50) REFERENCES users(user_id),
    match_score DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE quiz_results_public (
    result_id SERIAL PRIMARY KEY,
    display_name VARCHAR(50),
    city VARCHAR(100),
    personality_type VARCHAR(100),
    top_twin_names TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_business_id ON reviews(business_id);
CREATE INDEX idx_reviews_stars ON reviews(stars);
CREATE INDEX idx_businesses_city ON businesses(city);
CREATE INDEX idx_reviewer_profiles_rating ON reviewer_profiles(avg_rating);
CREATE INDEX idx_quiz_responses_created ON quiz_responses(created_at);
CREATE INDEX idx_quiz_results_created ON quiz_results_public(created_at DESC);
