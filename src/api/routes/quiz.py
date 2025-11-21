"""
Quiz submission endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Union, Any
import logging
from datetime import datetime

from ..kafka_producer import get_kafka_producer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

class QuizSubmission(BaseModel):
    display_name: str = Field(default="Anonymous", max_length=100)
    tags: Dict[str, Any] = Field(..., description="Quiz responses with mixed types")
    city: str = Field(default="Santa Barbara", max_length=100)
    state: str = Field(default="CA", max_length=50)

@router.post("/submit")
async def submit_quiz(submission: QuizSubmission):
    """Submit quiz responses"""
    try:
        quiz_message = {
            "display_name": submission.display_name,
            "quiz_tags": submission.tags,
            "city": submission.city,
            "state": submission.state,
            "submitted_at": datetime.utcnow().isoformat()
        }
        
        producer = get_kafka_producer()
        success = producer.publish_quiz_submission(quiz_message)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to process quiz")
        
        return {"status": "success", "message": "Quiz submitted!"}
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def quiz_health():
    return {"status": "healthy", "service": "quiz"}
