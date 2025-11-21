"""
Core matching algorithm to find taste twins
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class TasteTwinMatcher:
    """Find taste twins based on quiz responses"""
    
    def __init__(self):
        self.conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
    
    def find_taste_twins(
        self, 
        quiz_tags: Dict[str, Any], 
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find top N matching reviewers based on quiz responses
        
        Args:
            quiz_tags: User's quiz responses in tag format
            top_n: Number of matches to return
            
        Returns:
            List of matching reviewers with scores
        """
        
        # Get all reviewers with tags
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                u.user_id,
                u.name,
                u.review_count,
                u.tags
            FROM users u
            WHERE u.tags IS NOT NULL
        """)
        
        reviewers = cursor.fetchall()
        cursor.close()
        
        # Score each reviewer
        matches = []
        for reviewer in reviewers:
            # Tags is already a dict (JSONB automatically deserialized)
            reviewer_tags = reviewer['tags']
            score = self.calculate_similarity(quiz_tags, reviewer_tags)
            
            matches.append({
                'user_id': reviewer['user_id'],
                'name': reviewer['name'],
                'review_count': reviewer['review_count'],
                'score': score,
                'tags': reviewer_tags
            })
        
        # Sort by score and return top N
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:top_n]
    
    def calculate_similarity(
        self, 
        quiz_tags: Dict[str, Any], 
        reviewer_tags: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity score (0-100) between quiz and reviewer
        
        Scoring breakdown:
        - Priorities: 40 points (20 per match)
        - Dining style: 20 points (10 per match)
        - Meal timing: 10 points (up to 3 per match)
        - Cuisines: 15 points (5 per match, max 3)
        - Adventure level: 10 points (based on closeness)
        - Price sensitivity: 5 points (based on closeness)
        """
        
        score = 0.0
        
        # 1. Priorities match (40 points max)
        if quiz_tags.get('priorities') and reviewer_tags.get('priorities'):
            quiz_priorities = set(quiz_tags['priorities'])
            reviewer_priorities = set(reviewer_tags['priorities'])
            overlap = len(quiz_priorities & reviewer_priorities)
            score += overlap * 20  # 2 matches = 40 points
        
        # 2. Dining style match (20 points max)
        if quiz_tags.get('dining_style') and reviewer_tags.get('dining_style'):
            quiz_style = set(quiz_tags['dining_style'])
            reviewer_style = set(reviewer_tags['dining_style'])
            overlap = len(quiz_style & reviewer_style)
            score += overlap * 10  # 2 matches = 20 points
        
        # 3. Meal timing match (10 points max)
        if quiz_tags.get('meal_timing') and reviewer_tags.get('meal_timing'):
            quiz_meals = set(quiz_tags['meal_timing'])
            reviewer_meals = set(reviewer_tags['meal_timing'])
            overlap = len(quiz_meals & reviewer_meals)
            score += min(10, overlap * 3)  # Up to 10 points
        
        # 4. Cuisine match (15 points max)
        if quiz_tags.get('cuisines') and reviewer_tags.get('cuisine_preferences'):
            quiz_cuisines = set(quiz_tags['cuisines'])
            reviewer_cuisines = set(reviewer_tags['cuisine_preferences'])
            overlap = len(quiz_cuisines & reviewer_cuisines)
            score += min(15, overlap * 5)  # Max 3 matches = 15 points
        
        # 5. Adventure level match (10 points max)
        if quiz_tags.get('adventure_level') and reviewer_tags.get('adventure_level'):
            adventure_map = {
                'traditional': 1,
                'moderate': 2,
                'adventurous': 3,
                'very_adventurous': 4
            }
            quiz_adv = adventure_map.get(quiz_tags['adventure_level'], 2)
            reviewer_adv = adventure_map.get(reviewer_tags['adventure_level'], 2)
            diff = abs(quiz_adv - reviewer_adv)
            score += max(0, 10 - (diff * 3))  # Closer = more points
        
        # 6. Price sensitivity match (5 points max)
        if quiz_tags.get('price_sensitivity') and reviewer_tags.get('price_sensitivity'):
            price_map = {
                'budget': 1,
                'moderate': 2,
                'upscale': 3,
                'fine_dining': 4
            }
            quiz_price = price_map.get(quiz_tags['price_sensitivity'], 2)
            reviewer_price = price_map.get(reviewer_tags['price_sensitivity'], 2)
            diff = abs(quiz_price - reviewer_price)
            score += max(0, 5 - diff)
        
        return round(score, 2)
    
    def get_recommendations(
        self, 
        taste_twins: List[Dict[str, Any]], 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get restaurant recommendations based on taste twins
        
        Args:
            taste_twins: List of matched reviewers
            limit: Max number of restaurants to return
            
        Returns:
            List of recommended restaurants
        """
        
        twin_ids = [twin['user_id'] for twin in taste_twins]
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                b.business_id,
                b.name,
                b.address,
                b.city,
                b.stars as overall_stars,
                COUNT(r.review_id) as twin_endorsements,
                AVG(r.stars) as twin_avg_rating,
                STRING_AGG(DISTINCT r.user_id, ',') as endorsing_twins,
                ARRAY_AGG(r.text ORDER BY r.stars DESC) as sample_reviews
            FROM businesses b
            JOIN reviews r ON b.business_id = r.business_id
            WHERE r.user_id = ANY(%s)
            AND r.stars >= 4
            GROUP BY b.business_id, b.name, b.address, b.city, b.stars
            HAVING COUNT(r.review_id) >= 2
            ORDER BY twin_endorsements DESC, twin_avg_rating DESC
            LIMIT %s
        """, (twin_ids, limit))
        
        restaurants = cursor.fetchall()
        cursor.close()
        
        # Enrich with twin names
        for restaurant in restaurants:
            endorsing_ids = restaurant['endorsing_twins'].split(',')
            twin_names = [
                twin['name'] for twin in taste_twins 
                if twin['user_id'] in endorsing_ids
            ]
            restaurant['endorsing_twin_names'] = twin_names
            # Keep only first 2 sample reviews
            restaurant['sample_reviews'] = restaurant['sample_reviews'][:2]
        
        return restaurants
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
