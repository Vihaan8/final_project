"""
Integration tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_quiz_submit_valid_data():
    """Test quiz submission with valid data"""
    quiz_data = {
        "display_name": "Test User",
        "tags": {
            "priorities": ["food_quality", "atmosphere"],
            "dining_style": ["casual", "cozy"],
            "meal_timing": ["dinner"],
            "cuisines": ["italian", "mexican"],
            "adventure_level": "moderate",
            "price_sensitivity": "moderate"
        },
        "city": "Santa Barbara",
        "state": "CA"
    }
    
    response = client.post("/api/quiz/submit", json=quiz_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_quiz_submit_missing_fields():
    """Test quiz submission fails with missing required fields"""
    invalid_data = {
        "display_name": "Test User"
        # Missing tags, city, state
    }
    
    response = client.post("/api/quiz/submit", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_community_feed_endpoint():
    """Test community feed returns data"""
    response = client.get("/api/community/feed")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_community_stats_endpoint():
    """Test community stats returns correct structure"""
    response = client.get("/api/community/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_submissions" in data
    assert "today_submissions" in data
    assert "average_match_score" in data

def test_results_latest_endpoint():
    """Test results endpoint returns data structure"""
    response = client.get("/api/results/latest")
    
    # Should return 404 if no submissions, or 200 with data
    if response.status_code == 200:
        data = response.json()
        assert "taste_twins" in data
        assert "recommendations" in data
        assert "display_name" in data
    else:
        assert response.status_code == 404
