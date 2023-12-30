from datetime import datetime

from pydantic import ConfigDict, Field

from app.schema.base import Schema
from app.type.box import CityType


class _BoxBase(Schema):
    name: str = Field(description="이름")
    description: str = Field(description="설명")
    address: str = Field(description="주소")
    city: CityType = Field(description="도시")
    tel: str = Field(description="연락처")


class BoxCreate(_BoxBase):
    pass


class BoxResponse(_BoxBase):
    id: int = Field(description="아이디")
    created_at: datetime = Field(description="생성일시")
    updated_at: datetime = Field(description="수정일시")

    model_config = ConfigDict(from_attributes=True)
