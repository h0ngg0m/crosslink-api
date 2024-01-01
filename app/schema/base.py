from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from app.core.util import camelize


class Schema(BaseModel):
    model_config = ConfigDict(alias_generator=camelize, populate_by_name=True)
    # alias_generator: camelize 함수로 별칭을 만든다.
    # populate_by_name: alias로 지정한 이름으로 필드를 접근할 수 있게 해준다.


T = TypeVar("T")


class ListResponse(Schema, Generic[T]):
    page: int = Field(description="현재 페이지")
    items_per_page: int = Field(description="페이지 당 아이템 개수")
    items_length: int = Field(description="아이템 총 개수")
    items: list[T] = Field(description="아이템 목록")


class Meta(Schema):
    code: int = Field(200, description="응답 코드")
    message: str = Field("ok", description="응답 메세지")


class CommonResponse(Schema, Generic[T]):
    meta: Meta = Field(Meta(), description="메타 정보")
    data: T = Field(None, description="응답 데이터")
