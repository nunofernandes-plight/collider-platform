"""Configuration for API Gateway"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "Collider Platform API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC_COLLISION_EVENTS: str = 'collision-events'
    
    # PostgreSQL settings
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT', '5432'))
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'collider_db')
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'physics')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'quantum2024')
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Redis settings
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:8080", "http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    class Config:
        env_file = ".env"

settings = Settings()
