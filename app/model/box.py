from datetime import datetime

from sqlalchemy.orm import Mapped

from app.core.db.orm import Base, mapped_int_pk
from app.schema.box import BoxCreate
from app.type.box import CityType


class Box(Base):
    __tablename__ = "box"

    id: Mapped[mapped_int_pk]
    name: Mapped[str]
    description: Mapped[str]
    address: Mapped[str]
    city: Mapped[CityType]
    tel: Mapped[str]

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    @staticmethod
    def new(data: BoxCreate) -> "Box":
        return Box(
            **data.model_dump(exclude={"id"}),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
