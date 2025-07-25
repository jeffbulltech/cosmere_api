"""
Health check API endpoints.
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.database import get_db
from app.schemas.base import HealthResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the API."
)
async def health_check():
    """Basic health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="cosmere-api",
        version=settings.VERSION
    )


@router.get(
    "/db",
    response_model=HealthResponse,
    summary="Database health check",
    description="Check the health status of the database connection."
)
async def database_health_check(db: Session = Depends(get_db)):
    """Database health check endpoint."""
    try:
        # Simple query to test database connection
        db.execute("SELECT 1")
        return HealthResponse(
            status="healthy",
            service="cosmere-api-database",
            version=settings.VERSION
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            service="cosmere-api-database",
            version=settings.VERSION
        )


@router.get(
    "/detailed",
    response_model=dict,
    summary="Detailed health check",
    description="Get detailed health information for all services."
)
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check endpoint."""
    health_info = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": "cosmere-api",
        "version": settings.VERSION,
        "status": "healthy",
        "checks": {
            "database": {
                "status": "healthy",
                "message": "Database connection is working"
            },
            "api": {
                "status": "healthy",
                "message": "API is responding"
            }
        }
    }
    
    # Check database
    try:
        db.execute("SELECT 1")
        health_info["checks"]["database"]["status"] = "healthy"
    except Exception as e:
        health_info["checks"]["database"]["status"] = "unhealthy"
        health_info["checks"]["database"]["message"] = f"Database error: {str(e)}"
        health_info["status"] = "unhealthy"
    
    return health_info 