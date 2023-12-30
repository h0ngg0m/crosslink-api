from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_admin
from app.schema.admin import AdminAuthenticate, AdminCreate


def test_admin_login_success(client: TestClient, db: Session, admin_access_token: dict):
    # given
    data = {"name": "hong", "loginId": "cavok699", "password": "1234"}
    admin = crud_admin.create(db=db, data=AdminCreate(**data))
    crud_admin.update_authenticated(
        db=db, id_=admin.id, data=AdminAuthenticate(authenticated=True)
    )

    # when
    response = client.post(
        "api/v1/auth/admin/login",
        json={"loginId": "cavok699", "password": "1234"},
        headers=admin_access_token,
    )

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"

    response_data = response.json()["data"]
    assert response_data["accessToken"] is not None
    assert response_data["tokenType"] == "bearer"
