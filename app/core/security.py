from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_access_token(*, subject: str | Any, expires_delta: timedelta) -> str:
    to_encode = {"exp": datetime.now(timezone.utc) + expires_delta, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
