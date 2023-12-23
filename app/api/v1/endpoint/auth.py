from fastapi import APIRouter

from app.api.depends import SessionDepends
from app.crud import crud_user
from app.schema.auth import GoogleLogin
from app.schema.base import CommonResponse
from app.schema.token import Token

router = APIRouter()


@router.post("/login/google", response_model=CommonResponse[Token])
def google_login(db: SessionDepends, data: GoogleLogin):
    return CommonResponse(data=crud_user.google_login(db=db, data=data))
