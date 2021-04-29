from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from telethon import TelegramClient

# TODO: use dacite for config
# TODO: implement login and use a bot token taken from the user object
API_ID = 1078089
API_HASH = 'b9b273130eb150b628f8c20f338bb8a4'
BOT_TOKEN = '1749852619:AAHi0KZnbzy09FXKQ6TFhARH_zgsCXgTY0k'

bot = TelegramClient('bot', API_ID, API_HASH)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from app.routers.files import router
app.include_router(router)