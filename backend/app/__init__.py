import redis
import aioredis
from fastapi import FastAPI
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware import Middleware
from starlette_session import SessionMiddleware
from starlette_session.backends import BackendType
from starlette_wtf import CSRFProtectMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.db import TORTOISE_ORM
from app.dependencies.settings import get_settings

config = Config('.env')  # read config from .env file
settings = get_settings()

teleredis_connector = redis.Redis.from_url(settings.REDIS_URL)
redis_connector = aioredis.Redis.from_url(settings.REDIS_URL)


app = FastAPI(
    docs_url=None, redoc_url=None,
    middleware=[
        Middleware(
            SessionMiddleware,
            secret_key=settings.SECRET_KEY,
            cookie_name='session',
            backend_type=BackendType.redis,
            backend_client=teleredis_connector
        ),
        Middleware(
            CSRFProtectMiddleware,
            csrf_secret=settings.SECRET_KEY2
        )
    ]
)

oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

from app.routes import routers
from app.events import exceptions_handlers
from app.middlewares import LimitUploadSize

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


for router in routers:
    app.include_router(router)

for status_code, handler in exceptions_handlers.items():
    app.add_exception_handler(status_code, handler)

app.add_middleware(LimitUploadSize, max_upload_size=settings.MAX_UPLOAD_SIZE)

@app.on_event("startup")
async def create_redis():
    teleredis_connector.ping()
    await redis_connector

@app.on_event("shutdown")
async def close_redis():
    await redis_connector.close()
    teleredis_connector.close()
