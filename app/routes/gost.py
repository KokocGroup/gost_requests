from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from ..logic.gost import make_gost_request
from ..logic.cryptopro import crypto_pro_requester
from ..schemas.gost import GostRequestSchema, NbkiRequestSchema

gost_router = APIRouter()


@gost_router.post('/', status_code=200)
async def gost_request(data: GostRequestSchema):
    content = make_gost_request(data=data)
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK
    )


@gost_router.post('/nbki_request', status_code=200)
async def nbki_request(data: NbkiRequestSchema):
    content = crypto_pro_requester.make_nbki_request(data=data)
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK
    )
