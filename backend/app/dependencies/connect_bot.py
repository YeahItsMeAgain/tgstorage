from telethon import TelegramClient
from fastapi import Depends, Request
from teleredis import RedisSession
from telethon.errors.rpcerrorlist import AccessTokenInvalidError

from app import teleredis_connector
from app.settings import Settings
from app.dependencies.settings import get_settings

async def get_bot(bot_token: str, user_email: str, settings: Settings):
    session_name = f'{user_email}_{bot_token}'
    bot = TelegramClient(RedisSession(session_name, teleredis_connector), settings.API_ID, settings.API_HASH)
    if not bot.is_connected():
        await bot.start(bot_token=bot_token)
    return bot

async def connect_bot(request: Request, settings: Settings = Depends(get_settings)):
    bot_token = request.session.get('bot_token', None)
    if not bot_token:
        raise AccessTokenInvalidError('Invalid Access token')

    return await get_bot(bot_token, request.session["email"], settings)
