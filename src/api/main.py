"""
FastAPI main application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matching.matcher import TasteTwinMatcher

app = FastAPI(
    title="DineLike API",
    description="Find your taste twins and get personalized restaurant recommendations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizRequest(BaseModel):
    priorities: List[str] = Field(..., min_items=1, max_items=2)
    dining_style: List[str] = Field(..., min_items=1, max_items=2)
    meal_timing: List[str] = Field(..., min_items=0, max_items=4)
    cuisines: List[str] = Field(..., min_items=0, max_items=4)
    adventure_level: str
    price_sensitivity: str
    display_name: Optional[str] = "Anonymous"

class TwinReview(BaseModel):
    business_name: str
    stars: float
    text: str
    date: Optional[str]

class TasteTwin(BaseModel):
    user_id: str
    name: str
    review_count: int
    score: float
    matching_priorities: List[str]
    matching_styles: List[str]
    matching_cuisines: List[str]
    reviews: List[TwinReview]

class Restaurant(BaseModel):
    business_id: str
    name: str
    address: str
    city: str
    overall_stars: float
    twin_avg_rating: float
    twin_endorsements: int
    endorsing_twin_names: List[str]
    sample_reviews: List[str]

class QuizResponse(BaseModel):
    quiz_id: str
    taste_twins: List[TasteTwin]
    recommendations: List[Restaurant]

@app.get("/")
def root():
    return {
        "message": "Welcome to DineLike API",
        "docs": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/quiz/submit", response_model=QuizResponse)
def submit_quiz(quiz: QuizRequest):
    """Submit quiz and get taste twins + recommendations"""
    try:
        quiz_tags = {
            'priorities': quiz.priorities,
            'dining_style': quiz.dining_style,
            'meal_timing': quiz.meal_timing,
            'cuisines': quiz.cuisines,
            'adventure_level': quiz.adventure_level,
            'price_sensitivity': quiz.price_sensitivity
        }
        
        matcher = TasteTwinMatcher()
        taste_twins = matcher.find_taste_twins(quiz_tags, top_n=3)
        recommendations = matcher.get_recommendations(taste_twins, limit=20)
        
        formatted_twins = []
        for twin in taste_twins:
            twin_tags = twin['tags']
            twin_reviews = matcher.get_twin_reviews(twin['user_id'], limit=3)
            
            formatted_twins.append(TasteTwin(
                user_id=twin['user_id'],
                name=twin['name'],
                review_count=twin['review_count'],
                score=twin['score'],
                matching_priorities=list(set(quiz.priorities) & set(twin_tags.get('priorities', []))),
                matching_styles=list(set(quiz.dining_style) & set(twin_tags.get('dining_style', []))),
                matching_cuisines=list(set(quiz.cuisines) & set(twin_tags.get('cuisine_preferences', []))),
                reviews=[
                    TwinReview(
                        business_name=r['business_name'],
                        stars=float(r['stars']),
                        text=r['text'],
                        date=str(r['date']) if r.get('date') else None
                    )
                    for r in twin_reviews
                ]
            ))
        
        formatted_recs = [
            Restaurant(
                business_id=r['business_id'],
                name=r['name'],
                address=r['address'],
                city=r['city'],
                overall_stars=float(r['overall_stars']),
                twin_avg_rating=float(r['twin_avg_rating']),
                twin_endorsements=r['twin_endorsements'],
                endorsing_twin_names=r['endorsing_twin_names'],
                sample_reviews=r['sample_reviews']
            )
            for r in recommendations
        ]
        
        matcher.close()
        
        return QuizResponse(
            quiz_id="temp_id",
            taste_twins=formatted_twins,
            recommendations=formatted_recs
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
