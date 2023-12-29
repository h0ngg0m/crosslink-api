from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.box import Box
from app.schema.box import BoxCreate, BoxResponse


def get_boxes(*, db: Session) -> list[BoxResponse]:
    return [BoxResponse.model_validate(box) for box in db.scalars(select(Box)).all()]


def create(*, db: Session, data: BoxCreate) -> BoxResponse:
    box: Box = Box.new(data)

    db.add(box)
    db.commit()
    db.refresh(box)
    return BoxResponse.model_validate(box)
