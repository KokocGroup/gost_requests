import base64
import requests
import os
import subprocess
from fastapi.logger import logger
from io import BytesIO
from tempfile import NamedTemporaryFile
from ..schemas.gost import NbkiRequestSchema


class CryptoProRequester:

    def __init__(self):
        pass

    def make_nbki_request(self, data: NbkiRequestSchema):
        url = data.url
        method = data.method.upper()

        xml = base64.b64decode(data.xml_file)
        xml_file = NamedTemporaryFile(dir='/tmp', delete=False)
        xml_file.write(xml)
        xml_file_path = xml_file.name

        r = subprocess.run(f'/opt/cprocsp/bin/amd64/curl -X {method} -o - {url}  -E d6b6e0364b4229c2e1891cbe6e57e444e1d1cdb6 --connect-timeout 120 --max-time 120 -d {xml_file_path} -H "Content-Type: text/xml; charset=windows-1251;"', shell=True, capture_output=True)
        return r.stdout


crypto_pro_requester = CryptoProRequester()




