"""
Kafka producer for publishing quiz submissions and user activity events
"""
from kafka import KafkaProducer
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DineLikeKafkaProducer:
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        """Initialize Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',  # Wait for all replicas
                retries=3,
                max_in_flight_requests_per_connection=1
            )
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            raise

    def publish_quiz_submission(self, quiz_data: Dict[str, Any]) -> bool:
        """
        Publish quiz submission to Kafka
        
        Args:
            quiz_data: Dictionary containing quiz submission data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            future = self.producer.send('quiz-submissions', value=quiz_data)
            # Block until message is sent
            record_metadata = future.get(timeout=10)
            
            logger.info(
                f"Quiz submission published to topic '{record_metadata.topic}' "
                f"partition {record_metadata.partition} offset {record_metadata.offset}"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish quiz submission: {e}")
            return False

    def publish_user_activity(self, activity_data: Dict[str, Any]) -> bool:
        """
        Publish user activity event to Kafka
        
        Args:
            activity_data: Dictionary containing user activity data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            future = self.producer.send('user-activity', value=activity_data)
            record_metadata = future.get(timeout=10)
            
            logger.info(
                f"User activity published to topic '{record_metadata.topic}' "
                f"partition {record_metadata.partition} offset {record_metadata.offset}"
            )
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish user activity: {e}")
            return False

    def close(self):
        """Close Kafka producer"""
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")

# Global producer instance
_producer_instance = None

def get_kafka_producer() -> DineLikeKafkaProducer:
    """Get or create Kafka producer singleton"""
    global _producer_instance
    if _producer_instance is None:
        _producer_instance = DineLikeKafkaProducer()
    return _producer_instance
