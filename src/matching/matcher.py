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
        top_n: int = 3
    ) -> List[Dict[str, Any]]:
        """Find top N matching reviewers"""
        
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
        
        matches = []
        for reviewer in reviewers:
            reviewer_tags = reviewer['tags']
            score = self.calculate_similarity(quiz_tags, reviewer_tags)
            
            matches.append({
                'user_id': reviewer['user_id'],
                'name': reviewer['name'],
                'review_count': reviewer['review_count'],
                'score': score,
                'tags': reviewer_tags
            })
        
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:top_n]
    
    def calculate_similarity(
        self, 
        quiz_tags: Dict[str, Any], 
        reviewer_tags: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity score with CUISINE as highest weight
        
        Rebalanced scoring (Total: 100 points):
        - Cuisines: 30 points (HIGHEST)
        - Priorities: 30 points
        - Dining style: 15 points
        - Meal timing: 10 points
        - Adventure level: 10 points
        - Price sensitivity: 5 points
        """
        
        score = 0.0
        
        # 1. CUISINES - HIGHEST WEIGHT (30 points max)
        if quiz_tags.get('cuisines') and reviewer_tags.get('cuisine_preferences'):
            quiz_cuisines = set(quiz_tags['cuisines'])
            reviewer_cuisines = set(reviewer_tags['cuisine_preferences'])
            overlap = len(quiz_cuisines & reviewer_cuisines)
            score += min(30, overlap * 10)
        
        # 2. Priorities (30 points max)
        if quiz_tags.get('priorities') and reviewer_tags.get('priorities'):
            quiz_priorities = set(quiz_tags['priorities'])
            reviewer_priorities = set(reviewer_tags['priorities'])
            overlap = len(quiz_priorities & reviewer_priorities)
            score += overlap * 15
        
        # 3. Dining style (15 points max)
        if quiz_tags.get('dining_style') and reviewer_tags.get('dining_style'):
            quiz_style = set(quiz_tags['dining_style'])
            reviewer_style = set(reviewer_tags['dining_style'])
            overlap = len(quiz_style & reviewer_style)
            score += overlap * 7.5
        
        # 4. Meal timing (10 points max)
        if quiz_tags.get('meal_timing') and reviewer_tags.get('meal_timing'):
            quiz_meals = set(quiz_tags['meal_timing'])
            reviewer_meals = set(reviewer_tags['meal_timing'])
            overlap = len(quiz_meals & reviewer_meals)
            score += min(10, overlap * 3)
        
        # 5. Adventure level (10 points max)
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
            score += max(0, 10 - (diff * 3))
        
        # 6. Price sensitivity (5 points max)
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
        """Get restaurant recommendations based on taste twins"""
        
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
            HAVING COUNT(r.review_id) >= 1
            ORDER BY twin_endorsements DESC, twin_avg_rating DESC
            LIMIT %s
        """, (twin_ids, limit))
        
        restaurants = cursor.fetchall()
        cursor.close()
        
        for restaurant in restaurants:
            endorsing_ids = restaurant['endorsing_twins'].split(',')
            twin_names = [
                twin['name'] for twin in taste_twins 
                if twin['user_id'] in endorsing_ids
            ]
            restaurant['endorsing_twin_names'] = twin_names
            restaurant['sample_reviews'] = restaurant['sample_reviews'][:2]
        
        return restaurants
    
    def get_twin_reviews(self, twin_user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get actual reviews written by the taste twin"""
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                r.review_id,
                r.text,
                r.stars,
                r.date,
                b.name as business_name,
                b.address
            FROM reviews r
            JOIN businesses b ON r.business_id = b.business_id
            WHERE r.user_id = %s
            AND r.stars >= 4
            ORDER BY r.date DESC
            LIMIT %s
        """, (twin_user_id, limit))
        
        reviews = cursor.fetchall()
        cursor.close()
        return reviews
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
