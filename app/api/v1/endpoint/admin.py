from fastapi import APIRouter, Depends

from app.api.depends import AdminRoleChecker, SessionDepends
from app.crud import crud_admin
from app.schema.admin import AdminAuthenticate, AdminResponse
from app.schema.base import CommonResponse
from app.type.admin import AdminRole

router = APIRouter()


@router.get(
    "/{id_}",
    response_model=CommonResponse[AdminResponse],
    dependencies=[Depends(AdminRoleChecker(AdminRole.SUPER_ADMIN))],
)
async def read_by_id(db: SessionDepends, id_: int):
    return CommonResponse(data=crud_admin.read_by_id(db=db, id_=id_))


@router.patch(
    "/{id_}/authenticated",
    response_model=CommonResponse[AdminResponse],
    dependencies=[Depends(AdminRoleChecker(AdminRole.SUPER_ADMIN))],
)
async def update_authenticated(db: SessionDepends, id_: int, data: AdminAuthenticate):
    return CommonResponse(
        data=crud_admin.update_authenticated(db=db, data=data, id_=id_)
    )
