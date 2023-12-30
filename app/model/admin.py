from datetime import datetime

from sqlalchemy.orm import Mapped

from app.core.db.orm import Base, mapped_int_pk
from app.schema.admin import AdminAuthenticate, AdminCreate
from app.type.admin import AdminRole


class Admin(Base):
    __tablename__ = "admin"

    id: Mapped[mapped_int_pk]
    name: Mapped[str]
    login_id: Mapped[str]
    password: Mapped[str]
    authenticated: Mapped[bool]
    authenticated_at: Mapped[datetime | None]
    role: Mapped[AdminRole]

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    @staticmethod
    def new(data: AdminCreate) -> "Admin":
        return Admin(
            **data.model_dump(exclude={"id"}),
            authenticated=False,
            role=AdminRole.BASIC_ADMIN,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def authenticate(self, data: AdminAuthenticate) -> None:
        self.authenticated = data.authenticated
        self.authenticated_at = datetime.now()
