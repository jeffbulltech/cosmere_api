from fastapi import Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_user

# Dependency for database session
get_db_session = get_db

# Pagination dependency
class PaginationParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(20, ge=1, le=100, description="Number of items to return"),
    ):
        self.skip = skip
        self.limit = limit

# Common filter dependency (example for world_id)
def world_id_filter(world_id: Optional[str] = Query(None, description="Filter by world ID")):
    return world_id

# Auth dependencies (for endpoints that require authentication)
get_current_user_dep = Depends(get_current_user)
get_current_active_user_dep = Depends(get_current_active_user)

# Example: Admin check (expand as needed)
def require_admin(current_user=Depends(get_current_active_user)):
    # Implement your admin logic here
    if not current_user or not current_user.get("is_admin", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user

# Example: Rate limiting dependency (expand as needed)
def rate_limit(identifier: str):
    # Implement rate limiting logic here (e.g., using Redis)
    # Raise HTTPException if over limit
    pass 