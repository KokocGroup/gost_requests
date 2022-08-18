from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from ..logic.gost import make_gost_request
from ..schemas.gost import GostRequestSchema

gost_router = APIRouter()


@gost_router.post('/', status_code=200)
async def gost_request(data: GostRequestSchema):
    content = make_gost_request(data=data)
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK
    )
