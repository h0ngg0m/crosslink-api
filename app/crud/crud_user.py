from datetime import timedelta

from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.core.exception import ConflictException
from app.model.user import User
from app.schema.auth import GoogleLogin
from app.schema.token import Token
from app.schema.user import UserCreate, UserResponse
from app.type.auth import AuthType


def google_login(*, db: Session, data: GoogleLogin) -> Token:
    jwt: dict = id_token.verify_oauth2_token(
        data.credential,
        requests.Request(),
        settings.GOOGLE_CLIENT_ID,
    )
    user: User | None = db.query(User).filter_by(email=jwt["email"]).first()

    if not user:
        print("생성")
        user = User.new(
            UserCreate(email=jwt["email"], name=jwt["name"], auth_type=AuthType.GOOGLE)
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
