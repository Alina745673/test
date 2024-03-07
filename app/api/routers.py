from fastapi import APIRouter
from app.api.v1.posts import router as posts_router


v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(posts_router)
