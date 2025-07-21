from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def drop_tables():
    """Drop all tables in the database."""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise


def check_database_connection():
    """Check if database connection is working."""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


# Database health check
def get_database_health():
    """Get database health status."""
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT version()")
            version = result.fetchone()[0]
        return {
            "status": "healthy",
            "version": version,
            "connection": "active"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "connection": "failed"
        }


# Initialize database on startup
def init_database():
    """Initialize database connection and create tables if needed."""
    if check_database_connection():
        logger.info("Database initialized successfully")
    else:
        logger.error("Failed to initialize database")
        raise Exception("Database initialization failed") 