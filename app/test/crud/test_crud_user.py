import pytest
from sqlalchemy.orm import Session

from app.core.exception import ConflictException
from app.crud import crud_user
from app.schema.user import UserCreate


def test_create_success(db: Session):
    # given
    data = {"email": "jaehongbyeon98@gmail.com", "name": "변재홍", "authType": "GOOGLE"}

    # when
    user = crud_user.create(db=db, data=UserCreate(**data))

    # then
    assert user is not None
    assert user.id is not None
    assert user.email == "jaehongbyeon98@gmail.com"


def test_raise_conflict_exception_when_try_to_create_same_email_user(db: Session):
    # given
    data = {"email": "hong@gmail.com", "name": "hong", "authType": "GOOGLE"}
    crud_user.create(db=db, data=UserCreate(**data))

    # when, then
    data = {"email": "hong@gmail.com", "name": "honghong", "authType": "GOOGLE"}
    with pytest.raises(ConflictException) as error_info:
        crud_user.create(db=db, data=UserCreate(**data))
    assert error_info.value.args[0] == "'hong@gmail.com'는 이미 사용 중인 이메일입니다."
