"""
User results endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
import psycopg2
from pydantic import BaseModel

from ...matching.matcher import TasteTwinMatcher

router = APIRouter(prefix="/api/results", tags=["results"])

# Don't validate - just pass through what matcher returns
@router.get("/latest")
async def get_latest_results():
    """Get the most recent submission's results"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT submission_id
                FROM quiz_submissions
                ORDER BY created_at DESC
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="No submissions found")
            
            submission_id = row[0]
        
        conn.close()
        
        return await get_user_results(submission_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{submission_id}")
async def get_user_results(submission_id: int):
    """Get detailed results for a quiz submission"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT display_name, quiz_tags
                FROM quiz_submissions
                WHERE submission_id = %s
            """, (submission_id,))
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Submission not found")
            
            display_name = row[0]
            quiz_tags = row[1]
        
        conn.close()
        
        # Get taste twins and recommendations
        matcher = TasteTwinMatcher()
        taste_twins = matcher.find_taste_twins(quiz_tags, top_n=5)
        recommendations = matcher.get_recommendations(taste_twins, limit=10)
        matcher.close()
        
        # Return raw data without strict validation
        return {
            "submission_id": submission_id,
            "display_name": display_name,
            "taste_twins": taste_twins,
            "recommendations": recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
