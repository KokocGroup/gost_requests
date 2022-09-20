import base64
import subprocess
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

        xml = base64.b64decode(data.xml_file)
        xml_file = NamedTemporaryFile(dir='/tmp', delete=False)
        xml_file.write(xml)
        xml_file_path = xml_file.name

        connect_timeout = data.timeout
        max_time = data.max_time

        headers = data.headers
        headers = ' '.join([f'{i}: {j};' for i, j in headers.items()])

        response = str(subprocess.run(f'{settings.PATH_TO_CRYPTOPRO_CUR} -X {method} -o - {url}  -E {settings.CERTIFICATE_SHA1_THUMBPINT} --connect-timeout {connect_timeout} --max-time {max_time} -d {xml_file_path} -H "{headers} charset=windows-1251;"', shell=True, capture_output=True).stdout)
        soup = BeautifulSoup(response, 'lxml')
        result = soup.find('product')
        if result is not None:
            result = '<?xml version="1.0" encoding="windows-1251"?>' + result
            return result
        return False


crypto_pro_requester = CryptoProRequester()




