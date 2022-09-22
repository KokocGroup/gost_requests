import base64
import os
import subprocess
from fastapi.logger import logger
from tempfile import NamedTemporaryFile
from bs4 import BeautifulSoup
from ..schemas.gost import NbkiRequestSchema
from ..settings import settings


class CryptoProRequester:

    def __init__(self):
        pass

    def make_nbki_request(self, data: NbkiRequestSchema):
        url = data.url
        method = data.method.upper()

        xml = base64.b64decode(data.xml_file).decode(encoding='cp1251')
        xml_file = NamedTemporaryFile(mode='w+t', dir='/tmp', delete=False, suffix='.xml', encoding='cp1251')
        xml_file.write(xml)
        xml_file_path = xml_file.name

        connect_timeout = data.timeout
        max_time = data.max_time

        headers = data.headers
        headers = ' '.join([f'{i}: {j};' for i, j in headers.items()])

        response = str(subprocess.run(f'{settings.PATH_TO_CRYPTOPRO_CURL} -X{method} -o - -H "{headers} charset=windows-1251;" --upload-file {xml_file_path} -E {settings.CERTIFICATE_SHA1_THUMBPINT} --connect-timeout {connect_timeout} --max-time {max_time} {url}', shell=True, capture_output=True).stdout)
        logger.warning(f'{settings.PATH_TO_CRYPTOPRO_CURL} -X{method} -o - -H "{headers} charset=windows-1251;" --upload-file {xml_file_path} -E {settings.CERTIFICATE_SHA1_THUMBPINT} --connect-timeout {connect_timeout} --max-time {max_time} {url}')


        soup = BeautifulSoup(response, 'lxml')
        result = soup.find('product')

        if result is not None:
            result = '<?xml version="1.0" encoding="windows-1251"?>' + str(result)
            return result
        return False


crypto_pro_requester = CryptoProRequester()




