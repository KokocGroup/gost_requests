from pydantic import BaseModel
from typing import Optional, List, Union


class GostRequestSchema(BaseModel):
    url: str
    headers: Optional[dict]
    body: Optional[dict]
    verify: Optional[Union[bool, str]]
    cert: Optional[str]
    cert_key: Optional[str]
    method: str
    files: Optional[List[str]]

