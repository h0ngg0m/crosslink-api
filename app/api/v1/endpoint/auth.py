from fastapi import APIRouter

from app.api.depends import SessionDepends
from app.crud import crud_admin, crud_user
from app.schema.auth import AdminLogin, GoogleLogin, NaverLogin
from app.schema.base import CommonResponse
from app.schema.token import Token

router = APIRouter()


@router.post("/login/google", response_model=CommonResponse[Token])
async def google_login(db: SessionDepends, data: GoogleLogin):
    return CommonResponse(data=await crud_user.google_login(db=db, data=data))


@router.post("/login/naver", response_model=CommonResponse[Token])
async def naver_login(db: SessionDepends, data: NaverLogin):
    return CommonResponse(data=await crud_user.naver_login(db=db, data=data))


@router.post("/admin/login", response_model=CommonResponse[Token])
async def admin_login(db: SessionDepends, data: AdminLogin):
    return CommonResponse(data=crud_admin.login(db=db, data=data))
