from app.dependencies.settings import get_settings
from fastapi import Depends
from app import bot
from app.settings import Settings
async def connect_bot(settings: Settings = Depends(get_settings)):
    if not bot.is_connected():
        await bot.start(bot_token=settings.BOT_TOKEN)
    return bot
