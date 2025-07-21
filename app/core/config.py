from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "Cosmere API"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database
    database_url: str = Field(
        default="sqlite:///./cosmere.db",
        env="DATABASE_URL"
    )
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    # Elasticsearch
    elasticsearch_url: str = Field(
        default="http://localhost:9200",
        env="ELASTICSEARCH_URL"
    )
    elasticsearch_index_prefix: str = Field(
        default="cosmere",
        env="ELASTICSEARCH_INDEX_PREFIX"
    )
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-here",
        env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5240"],
        env="CORS_ORIGINS"
    )
    
    # Rate Limiting
    rate_limit_per_hour: int = Field(
        default=1000,
        env="RATE_LIMIT_PER_HOUR"
    )
    rate_limit_per_hour_authenticated: int = Field(
        default=10000,
        env="RATE_LIMIT_PER_HOUR_AUTHENTICATED"
    )
    
    # API
    api_v1_prefix: str = Field(default="/api/v1", env="API_V1_PREFIX")
    docs_url: Optional[str] = Field(default="/docs", env="DOCS_URL")
    redoc_url: Optional[str] = Field(default="/redoc", env="REDOC_URL")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Cache
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hour
    cache_prefix: str = Field(default="cosmere", env="CACHE_PREFIX")
    
    # Search
    search_max_results: int = Field(default=100, env="SEARCH_MAX_RESULTS")
    search_suggestions_limit: int = Field(default=10, env="SEARCH_SUGGESTIONS_LIMIT")
    
    # File Upload
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    
    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    
    # Development
    reload: bool = Field(default=False, env="RELOAD")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=5240, env="PORT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Validate required settings
def validate_settings():
    """Validate that all required settings are properly configured."""
    if settings.debug:
        print("⚠️  Running in DEBUG mode")
    
    if settings.secret_key == "your-secret-key-here":
        print("⚠️  Using default secret key. Please set SECRET_KEY in production.")
    
    # Ensure upload directory exists
    os.makedirs(settings.upload_dir, exist_ok=True)


# Call validation on import
validate_settings() 