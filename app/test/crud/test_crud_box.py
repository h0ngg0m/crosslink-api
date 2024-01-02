from sqlalchemy.orm import Session

from app.crud import crud_box
from app.schema.box import BoxCreate


def test_create_success(db: Session):
    # given
    data = {
        "name": "얼티밋 트레이닝",
        "description": "얼티밋 트레이닝 설명",
        "address": "서울시 강남구 역삼동 123-456",
        "city": "서울",
        "tel": "010-1234-5678",
    }

    # when
    box = crud_box.create(db=db, data=BoxCreate(**data))

    # then
    assert box is not None
    assert box.id is not None
    assert box.name == "얼티밋 트레이닝"
    assert box.description == "얼티밋 트레이닝 설명"
    assert box.address == "서울시 강남구 역삼동 123-456"
    assert box.city == "서울"
    assert box.tel == "010-1234-5678"


def test_get_boxes_success(db: Session):
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
    response = crud_box.get_boxes(
        db=db, page=1, items_per_page=100, sort_by=None, sort_order=None
    )
    boxes = response.items

    # then
    assert len(boxes) == 3
    assert boxes[0].id is not None
    assert boxes[0].name == "얼티밋 트레이닝 서울"
    assert boxes[0].description == "얼티밋 트레이닝 서울 설명"
    assert boxes[0].address == "서울시 강남구 역삼동 123-4561"
    assert boxes[0].city == "서울"
    assert boxes[0].tel == "010-1234-5678"
    assert boxes[0].created_at is not None
    assert boxes[0].updated_at is not None

    assert boxes[1].id is not None
    assert boxes[1].name == "얼티밋 트레이닝 대전"
    assert boxes[1].description == "얼티밋 트레이닝 대전 설명"
    assert boxes[1].address == "대전광역시 동구 삼성동 123-456"
    assert boxes[1].city == "대전"
    assert boxes[1].tel == "010-1234-7777"
    assert boxes[1].created_at is not None
    assert boxes[1].updated_at is not None

    assert boxes[2].id is not None
    assert boxes[2].name == "얼티밋 트레이닝 부산"
    assert boxes[2].description == "얼티밋 트레이닝 부산 설명"
    assert boxes[2].address == "부산광역시 해운대구 우동 123-456"
    assert boxes[2].city == "부산"
    assert boxes[2].tel == "010-1234-8888"
    assert boxes[2].created_at is not None
    assert boxes[2].updated_at is not None
