"""Redis cache operations"""
import redis
import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

class CacheHandler:
    """Handle Redis cache operations"""
    
    def __init__(self, host: str, port: int, db: int = 0):
        """Initialize Redis connection"""
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        logger.info(f"Redis connection initialized to {host}:{port}")
    
    def cache_event(self, event_id: str, data: dict, ttl: int = 3600) -> bool:
        """
        Cache event data
        
        Args:
            event_id: Event identifier
            data: Event data to cache
            ttl: Time to live in seconds (default 1 hour)
            
        Returns:
            Success status
        """
        try:
            key = f"event:{event_id}:processed"
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(data)
            )
            return True
        except Exception as e:
            logger.error(f"Failed to cache event: {e}")
            return False
    
    def get_event(self, event_id: str) -> Optional[dict]:
        """
        Retrieve cached event
        
        Args:
            event_id: Event identifier
            
        Returns:
            Cached data or None
        """
        try:
            key = f"event:{event_id}:processed"
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve cached event: {e}")
            return None
    
    def add_to_recent_events(self, event_id: str, score: float = None) -> bool:
        """
        Add event to recent events sorted set
        
        Args:
            event_id: Event identifier
            score: Score for sorting (timestamp if None)
            
        Returns:
            Success status
        """
        try:
            import time
            score = score or time.time()
            self.redis_client.zadd('live:recent_events', {event_id: score})
            
            # Keep only last 100 events
            self.redis_client.zremrangebyrank('live:recent_events', 0, -101)
            return True
        except Exception as e:
            logger.error(f"Failed to add to recent events: {e}")
            return False
    
    def get_recent_events(self, count: int = 10) -> list:
        """
        Get most recent events
        
        Args:
            count: Number of events to retrieve
            
        Returns:
            List of event IDs
        """
        try:
            events = self.redis_client.zrevrange('live:recent_events', 0, count - 1)
            return events
        except Exception as e:
            logger.error(f"Failed to get recent events: {e}")
            return []
    
    def increment_counter(self, key: str) -> int:
        """Increment a counter"""
        try:
            return self.redis_client.incr(key)
        except Exception as e:
            logger.error(f"Failed to increment counter: {e}")
            return 0
    
    def close(self):
        """Close Redis connection"""
        self.redis_client.close()
        logger.info("Redis connection closed")
