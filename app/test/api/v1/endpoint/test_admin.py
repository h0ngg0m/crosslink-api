from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_admin
from app.schema.admin import AdminCreate


def test_read_by_id_success(client: TestClient, db: Session, admin_access_token: dict):
    # given
    data = {"name": "hong", "loginId": "cavok699", "password": "1234"}
    admin = crud_admin.create(db=db, data=AdminCreate(**data))

    # when
    response = client.get(f"api/v1/admins/{admin.id}", headers=admin_access_token)

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"

    response_data = response.json()["data"]
    assert response_data["id"] == admin.id
    assert response_data["name"] == "hong"
    assert response_data["loginId"] == "cavok699"
    assert response_data["authenticated"] is False
    assert response_data["authenticatedAt"] is None
    assert response_data["role"] == "BASIC_ADMIN"
    assert response_data["createdAt"] is not None
    assert response_data["updatedAt"] is not None


def test_update_authenticated_success(
    client: TestClient, db: Session, admin_access_token: dict
):
    # given
    data = {"name": "hong", "loginId": "cavok699", "password": "1234"}
    created_admin = crud_admin.create(db=db, data=AdminCreate(**data))

    # when
    response = client.patch(
        f"api/v1/admins/{created_admin.id}/authenticated",
        headers=admin_access_token,
        json={"authenticated": True},
    )

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"

    response_data = response.json()["data"]
    assert response_data["id"] == created_admin.id
    assert response_data["name"] == "hong"
    assert response_data["loginId"] == "cavok699"
    assert response_data["authenticated"] is True
    assert response_data["authenticatedAt"] is not None
    assert response_data["role"] == "BASIC_ADMIN"
    assert response_data["createdAt"] is not None
    assert response_data["updatedAt"] is not None
