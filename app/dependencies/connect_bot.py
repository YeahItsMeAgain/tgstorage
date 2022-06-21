from telethon import TelegramClient
from fastapi import Depends, Request
from teleredis import RedisSession
from telethon.errors.rpcerrorlist import AccessTokenInvalidError

from app import redis_connector
from app.settings import Settings
from app.dependencies.settings import get_settings

async def connect_bot(request: Request, settings: Settings = Depends(get_settings)):
    bot_token = request.session.get('bot_token', None)
    if not bot_token:
        raise AccessTokenInvalidError('Invalid Access token')

    session_name = f'{request.session["email"]}_{bot_token}'
    bot = TelegramClient(RedisSession(session_name, redis_connector), settings.API_ID, settings.API_HASH)

    try:
        if not bot.is_connected():
            await bot.start(bot_token=bot_token)
    except AccessTokenInvalidError:
        del request.session['bot_token']
        raise
    return bot
