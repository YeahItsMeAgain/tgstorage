from pydantic import BaseSettings


class Settings(BaseSettings):
    API_ID: str
    API_HASH: str
    SECRET_KEY: str
    SECRET_KEY2: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
