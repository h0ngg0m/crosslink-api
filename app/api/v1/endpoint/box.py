from fastapi import APIRouter

from app.api.depends import SessionDepends
from app.crud import crud_box
from app.schema.base import CommonResponse
from app.schema.box import BoxResponse

router = APIRouter()


@router.get("", response_model=CommonResponse[list[BoxResponse]])
async def get_boxes(db: SessionDepends):
    return CommonResponse(data=crud_box.get_boxes(db=db))
