from pydantic import Field

from app.schema.base import Schema


class GoogleLogin(Schema):
    code: str = Field(..., description="구글 로그인 code")


class NaverLogin(Schema):
    code: str = Field(..., description="네이버 로그인 code")
    state: str = Field(..., description="네이버 로그인 state")
