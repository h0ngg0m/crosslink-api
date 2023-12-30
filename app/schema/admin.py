from datetime import datetime

from pydantic import ConfigDict, Field

from app.schema.base import Schema
from app.type.admin import AdminRole


class _AdminBase(Schema):
    name: str = Field(description="이름")
    login_id: str = Field(description="아이디")


class AdminCreate(_AdminBase):
    password: str = Field(description="비밀번호")


class AdminResponse(_AdminBase):
    id: int = Field(description="아이디")
    authenticated: bool = Field(description="인증 여부")
    authenticated_at: datetime | None = Field(description="인증 일시")
    role: AdminRole = Field(description="권한")

    created_at: datetime = Field(description="생성 일시")
    updated_at: datetime = Field(description="수정 일시")

    model_config = ConfigDict(from_attributes=True)


class AdminAuthenticate(Schema):
    authenticated: bool = Field(description="인증 여부")
