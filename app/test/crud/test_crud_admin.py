import pytest
from sqlalchemy.orm import Session

from app.core.exception import ConflictException
from app.crud import crud_admin
from app.model.admin import Admin
from app.schema.admin import AdminAuthenticate, AdminCreate
from app.schema.auth import AdminLogin


def test_create_success(db: Session):
    # given
    data = {"name": "hong", "loginId": "cavok699", "password": "1234"}

    # when
    admin = crud_admin.create(db=db, data=AdminCreate(**data))

    # then
    assert admin is not None
    assert admin.id is not None
    assert admin.name == "hong"
    assert admin.login_id == "cavok699"
    assert admin.authenticated is False
    assert admin.authenticated_at is None
    assert admin.role == "BASIC_ADMIN"
    assert admin.created_at is not None
    assert admin.updated_at is not None


def test_raise_conflict_exception_when_try_to_create_same_login_id_admin(db: Session):
    # given
    data = {"name": "hong", "loginId": "cavok699", "password": "1234"}
    crud_admin.create(db=db, data=AdminCreate(**data))

    # when, then
    data = {"name": "hong2", "loginId": "cavok699", "password": "1234"}
    with pytest.raises(ConflictException) as error_info:
        crud_admin.create(db=db, data=AdminCreate(**data))
    assert error_info.value.args[0] == "'cavok699'는 이미 사용 중인 아이디입니다."


def test_admin_login_success(db: Session):
    # given
    data = {"name": "hong", "loginId": "cavok699", "password": "1234"}
    admin_id = crud_admin.create(db=db, data=AdminCreate(**data)).id
    admin = db.get(Admin, admin_id)
    admin.authenticated = True
    db.add(admin)
    db.commit()

    # when
    token = crud_admin.login(
        db=db, data=AdminLogin(login_id="cavok699", password="1234")
    )

    # then
    assert token is not None


def test_read_by_id_success(db: Session):
    # given
    data = {"name": "hong", "loginId": "cavok699", "password": "1234"}
    admin = crud_admin.create(db=db, data=AdminCreate(**data))

    # when
    admin = crud_admin.read_by_id(db=db, id_=admin.id)

    # then
    assert admin is not None
    assert admin.id is not None
    assert admin.name == "hong"
    assert admin.login_id == "cavok699"
    assert admin.authenticated is False
    assert admin.authenticated_at is None
    assert admin.role == "BASIC_ADMIN"
    assert admin.created_at is not None
    assert admin.updated_at is not None


def test_update_authenticated_success(db: Session):
    # given
    data = {"name": "hong", "loginId": "cavok699", "password": "1234"}
    created_admin = crud_admin.create(db=db, data=AdminCreate(**data))

    # when
    admin = crud_admin.update_authenticated(
        db=db, id_=created_admin.id, data=AdminAuthenticate(authenticated=True)
    )

    # then
    assert admin is not None
    assert admin.id is not None
    assert admin.name == "hong"
    assert admin.login_id == "cavok699"
    assert admin.authenticated is True
    assert admin.authenticated_at is not None
    assert admin.role == "BASIC_ADMIN"
    assert admin.created_at is not None
    assert admin.updated_at is not None
