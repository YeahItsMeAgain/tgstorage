from fastapi import FastAPI
from telethon import TelegramClient
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware
from tortoise.contrib.fastapi import register_tortoise

# TODO: use dacite\starlette for config
# TODO: implement login and use a bot token taken from the user object
API_ID = 1078089
API_HASH = 'b9b273130eb150b628f8c20f338bb8a4'
BOT_TOKEN = '1749852619:AAHi0KZnbzy09FXKQ6TFhARH_zgsCXgTY0k'
SECRET_KEY = 'asfjafhbas8f7ha8sfha87hsfasf'

config = Config('.env')  # read config from .env file
bot = TelegramClient('bot', API_ID, API_HASH)
app = FastAPI(
    middleware=[
        Middleware(SessionMiddleware, secret_key=SECRET_KEY),
        Middleware(CSRFProtectMiddleware, csrf_secret=SECRET_KEY)
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

from app.events import exceptions_handlers
from app.routes import routers
from app.db import TORTOISE_ORM

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
