from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import get_settings

ALGORITHM = "HS256"

settings = get_settings()


def create_access_token(*, subject: dict, expires_delta: timedelta) -> str:
    subject.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(subject, settings.SECRET_KEY, algorithm=ALGORITHM)


def is_valid_jwt(token: str) -> bool:
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError:
        return False


def get_claims(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
