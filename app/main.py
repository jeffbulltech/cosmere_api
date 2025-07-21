from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging
from app.core.config import settings
from app.api.v1.api import api_router
import time

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger("cosmere_api")

app = FastAPI(
    title=settings.app_name,
    description="API for Brandon Sanderson's Cosmere universe",
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Logging and error handling middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = f"{request.method} {request.url.path}"
    logger.info(f"Request: {idem}")
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.exception(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error"},
        )
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Completed {idem} in {process_time:.2f}ms")
    return response

# Include aggregated API router
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "version": settings.app_version,
    }

# Test endpoint to check database
@app.get("/test-db", tags=["Test"])
def test_database():
    from app.core.database import SessionLocal
    from app.models.world import World
    
    db = SessionLocal()
    try:
        worlds = db.query(World).all()
        return {
            "status": "ok",
            "worlds_count": len(worlds),
            "worlds": [{"id": w.id, "name": w.name} for w in worlds]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close() 