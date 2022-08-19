from pydantic import BaseModel, Field
from typing import Optional, List, Union


class FileSchema(BaseModel):
    file_name: str
    file_string: str
    ext: Optional[str]
    param: str


class GostRequestSchema(BaseModel):
    url: str
    headers: Optional[dict]
    body: Optional[str]
    verify: Optional[Union[bool, str]]
    cert: Optional[str]
    cert_key: Optional[str]
    method: str
    files: Optional[List[FileSchema]]
    timeout: int = Field(default=30)

