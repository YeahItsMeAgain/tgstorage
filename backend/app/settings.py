from pydantic import BaseSettings


class Settings(BaseSettings):
    API_ID: str
    API_HASH: str
    SECRET_KEY: str
    SECRET_KEY2: str
    REDIS_URL: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    UPLOAD_EXPIRE_SECONDS: int
    MAX_UPLOAD_SIZE: int
    ALLOWED_MAILS: list

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
