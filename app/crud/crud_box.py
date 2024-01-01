from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count

from app.core.util import camel_to_snake
from app.model.box import Box
from app.schema.base import ListResponse
from app.schema.box import BoxCreate, BoxResponse


def get_boxes(
    *,
    db: Session,
    page: int,
    items_per_page: int,
    sort_by: str | None,
    sort_order: str | None
) -> ListResponse[BoxResponse]:
    select_query = select(Box)
    count_query = select(count(Box.id))

    if sort_by and sort_order:
        if sort_order == "desc":
            select_query = select_query.order_by(
                getattr(Box, camel_to_snake(sort_by)).desc()
            )
            count_query = count_query.order_by(
                getattr(Box, camel_to_snake(sort_by)).desc()
            )
        else:
            select_query = select_query.order_by(getattr(Box, camel_to_snake(sort_by)))
            count_query = count_query.order_by(getattr(Box, camel_to_snake(sort_by)))

    results = (
        db.scalars(
            select_query.limit(items_per_page).offset((page - 1) * items_per_page)
        )
    ).all()

    return ListResponse[BoxResponse](
        page=page,
        items_per_page=items_per_page,
        items_length=db.scalar(count_query.limit(1)),
        items=[BoxResponse.model_validate(box) for box in results],
    )


def create(*, db: Session, data: BoxCreate) -> BoxResponse:
    box: Box = Box.new(data)

    db.add(box)
    db.commit()
    db.refresh(box)
    return BoxResponse.model_validate(box)
