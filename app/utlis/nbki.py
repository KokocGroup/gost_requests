import asyncio
import os
import subprocess
from datetime import datetime
from fastapi.logger import logger
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient
from ..settings import settings

mongo = AsyncIOMotorClient(settings.MONGODB_CONNECT)
mongo.get_io_loop = asyncio.get_running_loop

mongo_db = mongo[settings.MONGODB_DATABASE]


async def log_nbki_response(result: str, _id: str):
    await mongo_db['nbki_results'].insert_one(
        {
            'request_id': _id,
            'result': result,
            'created_at': datetime.utcnow(),
        }
    )


async def get_nbki_result(_id: str):
    result = await mongo_db['nbki_results'].find_one(
        {
            'request_id': _id
        }
    )
    return result


async def send_nbki_request(cmd: str, xml_file_path: str, _id: str):
    response = str(subprocess.run(cmd, shell=True, capture_output=True).stdout)
    soup = BeautifulSoup(response, 'lxml')
    result = soup.find('product')
    logger.warning(result)
    await log_nbki_response(result=str(result), _id=_id)
    os.remove(xml_file_path)

