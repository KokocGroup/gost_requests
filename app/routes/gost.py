from fastapi import APIRouter, status, BackgroundTasks
from fastapi.responses import JSONResponse
from ..utlis.nbki import send_nbki_request, get_nbki_result
from ..logic.gost import make_gost_request
from ..logic.cryptopro import crypto_pro_requester
from ..schemas.gost import GostRequestSchema, NbkiRequestSchema, NbkiResultSchema

gost_router = APIRouter()


@gost_router.post('/', status_code=200)
async def gost_request(data: GostRequestSchema):
    content = make_gost_request(data=data)
    return JSONResponse(
        content=content,
        status_code=status.HTTP_200_OK
    )


@gost_router.post('/nbki_request', status_code=201)
async def nbki_request(data: NbkiRequestSchema, background_tasks: BackgroundTasks):
    cmd, xml_file_path, _id = crypto_pro_requester.make_nbki_request(data=data)
    background_tasks.add_task(send_nbki_request, cmd, xml_file_path, _id)
    return JSONResponse(
        content=_id,
        status_code=status.HTTP_201_CREATED
    )


@gost_router.post('/nbki_result', status_code=200)
async def nbki_result(request_id: str):
    result = await get_nbki_result(request_id)
    if result:
        return JSONResponse(
            content=result.get('result'),
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content='Not Found',
        status_code=status.HTTP_404_NOT_FOUND
    )
