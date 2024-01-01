from fastapi import APIRouter, Query

from app.api.depends import SessionDepends
from app.crud import crud_box
from app.schema.base import CommonResponse, ListResponse
from app.schema.box import BoxResponse

router = APIRouter()


@router.get("", response_model=CommonResponse[ListResponse[BoxResponse]])
async def get_boxes(
    db: SessionDepends,
    page: int = Query(),
    items_per_page: int = Query(),
    sort_by: str | None = Query(None),
    sort_order: str | None = Query(None),
):
    return CommonResponse(
        data=crud_box.get_boxes(
            db=db,
            page=page,
            items_per_page=items_per_page,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    )
