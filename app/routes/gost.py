from fastapi import APIRouter
from ..logic.gost import make_gost_request
from ..schemas.gost import GostRequestSchema

gost_router = APIRouter()


@gost_router.post('/')
async def gost_request(data: GostRequestSchema):
    return make_gost_request(data=data)
