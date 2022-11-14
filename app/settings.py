from pydantic import BaseSettings


class Settings(BaseSettings):
    PATH_TO_CRYPTOPRO_CURL: str
    CERTIFICATE_SHA1_THUMBPINT: str
    MONGODB_CONNECT: str
    MONGODB_DATABASE: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)