from pydantic import BaseSettings


class Env(BaseSettings):
    FILTER_MODULE: str
    FILTER_HOST: str = "127.0.0.1"
    FILTER_PORT: int
    ENGINE_MODULE: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Config(BaseSettings):
    pass
