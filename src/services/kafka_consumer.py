"""
Kafka consumer for processing quiz submissions
"""
from kafka import KafkaConsumer
import json
import logging
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matching.matcher import TasteTwinMatcher
import psycopg2
from psycopg2.extras import Json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class QuizConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'quiz-submissions',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='quiz-processing-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        self.matcher = TasteTwinMatcher()
        
        self.conn = psycopg2.connect(
            host='localhost',
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        self.conn.autocommit = True
        logger.info("Kafka consumer initialized")

    def process_quiz_submission(self, message):
        try:
            logger.info(f"Processing quiz: {message.get('display_name', 'Anonymous')}")
            
            # Use the existing matcher to find taste twins
            quiz_tags = message['quiz_tags']
            taste_twins = self.matcher.find_taste_twins(quiz_tags, top_n=1)
            
            if taste_twins and len(taste_twins) > 0:
                top_twin = taste_twins[0]
                match_result = {
                    "twin_user_id": top_twin['user_id'],
                    "twin_name": top_twin['name'],
                    "match_score": top_twin['score']
                }
                logger.info(f"Found taste twin: {match_result['twin_name']} ({match_result['match_score']}%)")
            else:
                match_result = {
                    "twin_user_id": "no_match",
                    "twin_name": "No Match Found",
                    "match_score": 0.0
                }
                logger.warning("No taste twins found")
            
            # Insert into database
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO quiz_submissions 
                    (display_name, quiz_tags, top_twin_user_id, top_twin_name, 
                     match_score, city, state, processing_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING submission_id
                """, (
                    message.get('display_name', 'Anonymous'),
                    Json(quiz_tags),
                    match_result['twin_user_id'],
                    match_result['twin_name'],
                    match_result['match_score'],
                    message.get('city', 'Santa Barbara'),
                    message.get('state', 'CA'),
                    'completed'
                ))
                submission_id = cursor.fetchone()[0]
                
            logger.info(f"✅ Processed! ID: {submission_id}, Match: {match_result['twin_name']} ({match_result['match_score']}%)")
            
        except Exception as e:
            logger.error(f"Error processing: {e}", exc_info=True)

    def run(self):
        logger.info("🚀 Kafka consumer started - waiting for messages...")
        try:
            for message in self.consumer:
                self.process_quiz_submission(message.value)
        except KeyboardInterrupt:
            logger.info("Consumer stopped")
        finally:
            self.consumer.close()
            self.matcher.close()
            self.conn.close()

if __name__ == "__main__":
    consumer = QuizConsumer()
    consumer.run()
