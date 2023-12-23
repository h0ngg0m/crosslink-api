from pydantic import Field

from app.schema.base import Schema


class GoogleLogin(Schema):
    credential: str = Field(..., description="구글 로그인 정보")
