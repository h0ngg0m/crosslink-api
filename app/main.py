from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.api.v1.api import api_v1_router
from app.core.exception import CustomException
from app.schema.base import camelize

app = FastAPI()

app.include_router(api_v1_router)

for route in app.routes:
    if isinstance(route, APIRoute):
        for param in route.dependant.query_params:
            param.field_info.alias = camelize(param.name)


# openapi docs (swagger) 에서 기본으로 포함되는 422 에러를 제거하기 위한 코드
def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get("paths").items():
            for _, param in method_item.items():
                responses = param.get("responses")
                if "422" in responses:
                    del responses["422"]
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content=jsonable_encoder(
            {"meta": {"code": exc.code, "message": exc.message}, "data": None}
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"Full error details: {exc.errors()}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "meta": {
                    "code": HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": "올바르지 않은 입력값입니다.",
                },
                "data": None,
            }
        ),
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {"meta": {"code": exc.status_code, "message": exc.detail}, "data": None}
        ),
    )


origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:8082",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
