"""Configuration for analysis service"""
import os

class Config:
    """Service configuration"""
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC_COLLISION_EVENTS = 'collision-events'
    KAFKA_TOPIC_PROCESSED_EVENTS = 'processed-events'
    KAFKA_GROUP_ID = 'analysis-service'
    
    # PostgreSQL settings
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'collider_db')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'physics')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'quantum2024')
    
    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Redis settings
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    
    # Analysis settings
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '100'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

config = Config()
