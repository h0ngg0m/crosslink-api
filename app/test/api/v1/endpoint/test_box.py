from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import crud_box
from app.schema.box import BoxCreate


def test_get_boxes_success(client: TestClient, db: Session):
    # given
    data1 = {
        "name": "얼티밋 트레이닝 서울",
        "description": "얼티밋 트레이닝 서울 설명",
        "address": "서울시 강남구 역삼동 123-4561",
        "city": "서울",
        "tel": "010-1234-5678",
    }
    data2 = {
        "name": "얼티밋 트레이닝 대전",
        "description": "얼티밋 트레이닝 대전 설명",
        "address": "대전광역시 동구 삼성동 123-456",
        "city": "대전",
        "tel": "010-1234-7777",
    }
    data3 = {
        "name": "얼티밋 트레이닝 부산",
        "description": "얼티밋 트레이닝 부산 설명",
        "address": "부산광역시 해운대구 우동 123-456",
        "city": "부산",
        "tel": "010-1234-8888",
    }
    crud_box.create(db=db, data=BoxCreate(**data1))
    crud_box.create(db=db, data=BoxCreate(**data2))
    crud_box.create(db=db, data=BoxCreate(**data3))

    # when
    response = client.get("api/v1/boxes?page=1&itemsPerPage=100&sortBy=&sortOrder=")

    # then
    assert response.status_code == 200
    assert response.json()["meta"]["code"] == 200
    assert response.json()["meta"]["message"] == "ok"

    response_data = response.json()["data"]["items"]
    assert len(response_data) == 3

    assert response_data[0]["id"] is not None
    assert response_data[0]["name"] == "얼티밋 트레이닝 서울"
    assert response_data[0]["description"] == "얼티밋 트레이닝 서울 설명"
    assert response_data[0]["address"] == "서울시 강남구 역삼동 123-4561"
    assert response_data[0]["city"] == "서울"
    assert response_data[0]["tel"] == "010-1234-5678"
    assert response_data[0]["createdAt"] is not None
    assert response_data[0]["updatedAt"] is not None

    assert response_data[1]["id"] is not None
    assert response_data[1]["name"] == "얼티밋 트레이닝 대전"
    assert response_data[1]["description"] == "얼티밋 트레이닝 대전 설명"
    assert response_data[1]["address"] == "대전광역시 동구 삼성동 123-456"
    assert response_data[1]["city"] == "대전"
    assert response_data[1]["tel"] == "010-1234-7777"
    assert response_data[1]["createdAt"] is not None
    assert response_data[1]["updatedAt"] is not None

    assert response_data[2]["id"] is not None
    assert response_data[2]["name"] == "얼티밋 트레이닝 부산"
    assert response_data[2]["description"] == "얼티밋 트레이닝 부산 설명"
    assert response_data[2]["address"] == "부산광역시 해운대구 우동 123-456"
    assert response_data[2]["city"] == "부산"
    assert response_data[2]["tel"] == "010-1234-8888"
    assert response_data[2]["createdAt"] is not None
    assert response_data[2]["updatedAt"] is not None
