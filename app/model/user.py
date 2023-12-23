from datetime import datetime

from sqlalchemy.orm import Mapped

from app.core.db.orm import Base, mapped_int_pk
from app.schema.user import UserCreate
from app.type.auth import AuthType


class User(Base):
    __tablename__ = "user"

    id: Mapped[mapped_int_pk]
    email: Mapped[str]
    name: Mapped[str]
    auth_type: Mapped[AuthType]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    @staticmethod
    def new(data: UserCreate) -> "User":
        return User(
            **data.model_dump(exclude={"id"}),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
