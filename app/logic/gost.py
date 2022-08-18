import base64
import requests
import traceback
from io import BytesIO
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
from fastapi import HTTPException
from ..schemas.gost import GostRequestSchema

CIPHERS = (
        'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:'
        'ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:'
        'DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:'
        'ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:DHE-RSA-AES256-SHA256:ECDHE-ECDSA-AES128-SHA256:'
        'ECDHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES256-SHA:'
        'ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES128-SHA:RSA-PSK-AES256-GCM-SHA384:DHE-PSK-AES256-GCM-SHA384:'
        'RSA-PSK-CHACHA20-POLY1305:DHE-PSK-CHACHA20-POLY1305:ECDHE-PSK-CHACHA20-POLY1305:AES256-GCM-SHA384:PSK-AES256-GCM-SHA384:'
        'PSK-CHACHA20-POLY1305:RSA-PSK-AES128-GCM-SHA256:DHE-PSK-AES128-GCM-SHA256:AES128-GCM-SHA256:PSK-AES128-GCM-SHA256:AES256-SHA256:'
        'AES128-SHA256:ECDHE-PSK-AES256-CBC-SHA384:ECDHE-PSK-AES256-CBC-SHA:SRP-RSA-AES-256-CBC-SHA:SRP-AES-256-CBC-SHA:'
        'RSA-PSK-AES256-CBC-SHA384:DHE-PSK-AES256-CBC-SHA384:RSA-PSK-AES256-CBC-SHA:DHE-PSK-AES256-CBC-SHA:GOST2012-GOST8912-GOST8912:'
        'GOST2001-GOST89-GOST89:AES256-SHA:PSK-AES256-CBC-SHA384:PSK-AES256-CBC-SHA:ECDHE-PSK-AES128-CBC-SHA256:ECDHE-PSK-AES128-CBC-SHA:'
        'SRP-RSA-AES-128-CBC-SHA:SRP-AES-128-CBC-SHA:RSA-PSK-AES128-CBC-SHA256:DHE-PSK-AES128-CBC-SHA256:RSA-PSK-AES128-CBC-SHA:DHE-PSK-AES128-CBC-SHA:'
        'AES128-SHA:PSK-AES128-CBC-SHA256:PSK-AES128-CBC-SHA'
)


class GOSTAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(GOSTAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(GOSTAdapter, self).proxy_manager_for(*args, **kwargs)


def make_gost_request(data: GostRequestSchema):
    url = data.url
    headers = data.headers
    body = data.body
    verify = data.verify
    cert = data.cert
    cert_key = data.cert_key
    method = data.method.upper()
    files = data.files
    timeout = data.timeout

    s = requests.Session()

    if verify is not None:
        if isinstance(verify, str):
            verify = base64.b64decode(verify).decode()
        s.verify = verify

    if cert:
        cert = base64.b64decode(data.cert).decode()
        if cert_key:
            cert_key = base64.b64decode(data.cert_key).decode()
            s.cert = (cert, cert_key)
        else:
            s.cert = cert

    if files:
        files = {file.param: (file.file_name, BytesIO(base64.b64decode(file.file_string)), file.ext) for file in files}

    s.mount(url, GOSTAdapter())
    try:
        r = s.request(method=method, url=url, data=body, headers=headers, files=files, timeout=timeout)
        status_code = r.status_code
        result = r.text
        s.close()
        return {
            'status': status_code,
            'result': result
        }
    except requests.exceptions.ConnectTimeout:
        raise HTTPException(status_code=400, detail='Connection timeout')
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=400, detail=f'No route to host {url}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))

