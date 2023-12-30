from typing import Annotated, Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core import security
from app.core.config import settings
from app.core.db.session import SessionLocal
from app.core.exception import (
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from app.core.security import get_claims, is_valid_jwt
from app.model.user import User
from app.schema.token import TokenPayload
from app.type.admin import AdminRole


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDepends = Annotated[Session, Depends(get_db)]


# 요청한 토큰을 디코딩하여 유저 정보를 가져온다.
def get_current_user(session: SessionDepends, request: Request) -> User:
    try:
        authorization = request.headers.get("Authorization")

        if not authorization or len(authorization.split(" ")) != 2:
            raise UnauthorizedException("권한이 없습니다.")

        token = authorization.split(" ")[1]

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )

        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise UnauthorizedException("권한이 없습니다.")

    user: User | None = session.get(User, token_data.sub)

    if not user:
        raise NotFoundException("존재하지 않는 회원입니다.")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


class VerifyJWT(HTTPBearer):
    async def __call__(
        self,
        request: Request,
    ):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise UnauthorizedException("권한이 없습니다.")

        access_token = credentials.credentials
        if not access_token:
            raise UnauthorizedException("권한이 없습니다.")

        if not is_valid_jwt(access_token):
            raise UnauthorizedException("권한이 없습니다.")

        return request


verify_jwt = VerifyJWT()


class AdminRoleChecker:
    def __init__(self, required_role: AdminRole | None = None):
        self.required_role = required_role

    async def __call__(
        self,
        request=Depends(verify_jwt),
    ):
        access_token = request.headers.get("Authorization")[7:]
        claims = get_claims(access_token)

        admin_role = claims.get("role")
        admin_login_id = claims.get("login_id")

        if admin_role is None:
            raise ForbiddenException("권한이 없습니다.")

        if admin_role == AdminRole.SUPER_ADMIN or admin_login_id == "admin":
            return request

        if self.required_role is None:
            return request

        if self.required_role != admin_role:
            raise ForbiddenException("권한이 없습니다.")

        return request
