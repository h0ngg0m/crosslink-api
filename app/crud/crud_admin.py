from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import get_settings
from app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)
from app.core.security import get_password_hash, verify_password
from app.model.admin import Admin
from app.schema.admin import AdminAuthenticate, AdminCreate, AdminResponse
from app.schema.auth import AdminLogin
from app.schema.token import AdminClaim, Token

settings = get_settings()


def read_by_id(*, db: Session, id_: int) -> AdminResponse | None:
    admin: Admin = db.scalar(select(Admin).filter_by(id=id_).limit(1))
    return AdminResponse.model_validate(admin) if admin else None


def create(*, db: Session, data: AdminCreate) -> AdminResponse:
    same_login_id_admin: Admin | None = (
        db.query(Admin).filter_by(login_id=data.login_id).first()
    )

    if same_login_id_admin:
        raise ConflictException(f"'{data.login_id}'는 이미 사용 중인 아이디입니다.")

    admin: Admin = Admin.new(data)
    admin.password = get_password_hash(admin.password)

    db.add(admin)
    db.commit()
    db.refresh(admin)
    return AdminResponse.model_validate(admin)


def login(*, db: Session, data: AdminLogin) -> Token:
    admin: Admin = db.scalar(select(Admin).filter_by(login_id=data.login_id).limit(1))

    if not admin or not verify_password(
        plain_password=data.password, hashed_password=admin.password
    ):
        raise BadRequestException("잘못된 아이디 혹은 비밀번호입니다.")

    if not admin.authenticated:
        raise UnauthorizedException("인증되지 않은 관리자입니다.")

    return Token(
        access_token=security.create_access_token(
            subject=AdminClaim.from_admin(admin).model_dump(),
            expires_delta=timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
        ),
        token_type="bearer",
    )


def update_authenticated(
    *, db: Session, id_: int, data: AdminAuthenticate
) -> AdminResponse:
    admin: Admin = db.scalar(select(Admin).filter_by(id=id_).limit(1))

    if not admin:
        raise NotFoundException("존재하지 않는 관리자입니다.")

    admin.authenticate(data)

    db.add(admin)
    db.commit()
    db.refresh(admin)
    return AdminResponse.model_validate(admin)
