from datetime import datetime

from pydantic import ConfigDict, Field

from app.schema.base import Schema
from app.type.auth import AuthType


class _UserBase(Schema):
    email: str = Field(description="이메일")
    name: str = Field(description="이름")
    auth_type: AuthType = Field(description="인증 타입")


class UserCreate(_UserBase):
    pass


class UserResponse(_UserBase):
    id: int = Field(description="아이디")
    created_at: datetime = Field(description="생성일시")
    updated_at: datetime = Field(description="수정일시")

    model_config = ConfigDict(from_attributes=True)
