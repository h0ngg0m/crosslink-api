from fastapi import APIRouter

from app.api.v1.endpoint import auth

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
