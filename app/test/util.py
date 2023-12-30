from datetime import timedelta
from typing import Dict

from sqlalchemy.orm import Session

from app.core import security
from app.crud import crud_admin, crud_user
from app.schema.admin import AdminCreate
from app.schema.user import UserCreate


def get_user_access_token(db: Session) -> Dict[str, str]:
    data = {"email": "admin@gmail.com", "name": "admin", "authType": "GOOGLE"}
    user = crud_user.create(db=db, data=UserCreate(**data))
    access_token = security.create_access_token(
        subject=user.id,
        expires_delta=timedelta(hours=1),
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def get_admin_access_token(db: Session) -> Dict[str, str]:
    data = {"name": "admin", "loginId": "admin", "password": "1234"}
    admin = crud_admin.create(db=db, data=AdminCreate(**data))
    access_token = security.create_access_token(
        subject={"id": admin.id, "login_id": admin.login_id, "role": admin.role},
        expires_delta=timedelta(hours=1),
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers
