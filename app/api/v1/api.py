from fastapi import APIRouter

from app.api.v1.endpoint import admin, auth, box

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
api_v1_router.include_router(box.router, prefix="/api/v1/boxes", tags=["Box"])
api_v1_router.include_router(admin.router, prefix="/api/v1/admins", tags=["Admin"])
