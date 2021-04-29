from app import bot, BOT_TOKEN

async def connect_bot():
    if not bot.is_connected():
        await bot.start(BOT_TOKEN)
    return bot
