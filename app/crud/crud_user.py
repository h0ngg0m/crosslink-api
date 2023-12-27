from datetime import timedelta

import aiohttp
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.core.exception import ConflictException
from app.model.user import User
from app.schema.auth import GoogleLogin, NaverLogin
from app.schema.token import Token
from app.schema.user import UserCreate, UserResponse
from app.type.auth import AuthType


async def google_login(*, db: Session, data: GoogleLogin) -> Token:
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        async with session.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": data.code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_CALLBACK_URL,
                "grant_type": "authorization_code",
            },
        ) as response:
            user_info = await response.json()

            jwt: dict = id_token.verify_oauth2_token(
                user_info["id_token"],
                requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )

            user: User | None = db.query(User).filter_by(email=jwt["email"]).first()

            if not user:
                user = User.new(
                    UserCreate(
                        email=jwt["email"], name=jwt["name"], auth_type=AuthType.GOOGLE
                    )
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            return Token(
                access_token=security.create_access_token(
                    subject=user.id,
                    expires_delta=timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
                ),
                token_type="bearer",
            )


async def naver_login(*, db: Session, data: NaverLogin) -> Token:
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        async with session.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={settings.NAVER_CLIENT_ID}&client_secret={settings.NAVER_CLIENT_SECRET}&code={data.code}&state={data.state}"
        ) as response:
            data = await response.json()
        async with session.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {data['access_token']}"},
        ) as response:
            user_info = await response.json()
            user_info = user_info["response"]

            user: User | None = (
                db.query(User).filter_by(email=user_info["email"]).first()
            )

            if not user:
                user = User.new(
                    UserCreate(
                        email=user_info["email"],
                        name=user_info["name"],
                        auth_type=AuthType.GOOGLE,
                    )
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            return Token(
                access_token=security.create_access_token(
                    subject=user.id,
                    expires_delta=timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
                ),
                token_type="bearer",
            )


def create(*, db: Session, data: UserCreate) -> UserResponse:
    same_email_user: User | None = db.query(User).filter_by(email=data.email).first()

    if same_email_user:
        raise ConflictException(f"'{data.email}'는 이미 사용 중인 이메일입니다.")

    user: User = User.new(data)

    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)
