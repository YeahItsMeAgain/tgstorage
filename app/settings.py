from pydantic import BaseSettings


class Settings(BaseSettings):
    API_ID: str
    API_HASH: str
    BOT_TOKEN: str
    SECRET_KEY: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
