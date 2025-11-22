"""
Unit tests for TasteTwinMatcher
"""
import pytest
from src.matching.matcher import TasteTwinMatcher

def test_calculate_similarity_exact_match():
    """Test that identical preferences give high score"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian', 'mexican'],
        'priorities': ['food_quality', 'atmosphere'],
        'dining_style': ['casual', 'cozy'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian', 'mexican'],
        'priorities': ['food_quality', 'atmosphere'],
        'dining_style': ['casual', 'cozy'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score = matcher.calculate_similarity(quiz_tags, reviewer_tags)
    matcher.close()
    
    # Exact match should give highest possible score (around 83% based on your scoring)
    assert score >= 80.0, f"Expected high match (>=80), got {score}"
    assert score <= 100.0, f"Score should not exceed 100, got {score}"

def test_calculate_similarity_no_match():
    """Test that completely different preferences give low score"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['upscale'],
        'meal_timing': ['dinner'],
        'adventure_level': 'traditional',
        'price_sensitivity': 'fine_dining'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['chinese'],
        'priorities': ['value'],
        'dining_style': ['casual'],
        'meal_timing': ['breakfast'],
        'adventure_level': 'very_adventurous',
        'price_sensitivity': 'budget'
    }
    
    score = matcher.calculate_similarity(quiz_tags, reviewer_tags)
    matcher.close()
    
    assert score < 30.0, f"Expected low match (<30), got {score}"

def test_calculate_similarity_partial_match():
    """Test partial overlap gives medium score"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian', 'mexican'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['upscale'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'upscale'
    }
    
    score = matcher.calculate_similarity(quiz_tags, reviewer_tags)
    matcher.close()
    
    assert 40 < score < 70, f"Expected medium match (40-70), got {score}"

def test_better_cuisine_match_scores_higher():
    """Test that more cuisine overlap increases score"""
    matcher = TasteTwinMatcher()
    
    quiz = {
        'cuisines': ['italian', 'mexican', 'japanese'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    # Reviewer with 3 cuisine matches
    reviewer_high = {
        'cuisine_preferences': ['italian', 'mexican', 'japanese'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    # Reviewer with 1 cuisine match
    reviewer_low = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score_high = matcher.calculate_similarity(quiz, reviewer_high)
    score_low = matcher.calculate_similarity(quiz, reviewer_low)
    matcher.close()
    
    assert score_high > score_low, f"More cuisine matches ({score_high}) should score higher than fewer ({score_low})"

def test_empty_arrays_dont_crash():
    """Test that empty preference arrays are handled gracefully"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': [],
        'priorities': [],
        'dining_style': [],
        'meal_timing': [],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score = matcher.calculate_similarity(quiz_tags, reviewer_tags)
    matcher.close()
    
    # Should return a score, not crash
    assert isinstance(score, (int, float))
    assert 0 <= score <= 100
