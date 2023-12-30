from pydantic import Field

from app.model.admin import Admin
from app.schema.base import Schema
from app.type.admin import AdminRole


class Token(Schema):
    access_token: str = Field(description="액세스 토큰")
    token_type: str = Field(description="토큰 종류")


class TokenPayload(Schema):
    sub: int | None = Field(None, description="토큰 내용")


class AdminClaim(Schema):
    id: int
    login_id: str
    role: AdminRole

    @classmethod
    def from_admin(cls, admin: Admin):
        return cls(id=admin.id, login_id=admin.login_id, role=admin.role)
