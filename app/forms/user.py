from starlette_wtf import StarletteForm
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AccessTokenInvalidError
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
import uuid

from app.dependencies.settings import get_settings

class GetUserBotTokenForm(StarletteForm):
    bot_token = StringField(
        'Bot Token',
        validators=[
            DataRequired('Please enter a valid bot token'),
        ]
    )

    async def async_validate_bot_token(self, bot_token, settings= get_settings()):
        client = TelegramClient(str(uuid.uuid4()), settings.API_ID, settings.API_HASH)
        try:
            await client.start(bot_token=bot_token.data)
            await client.log_out()
        except AccessTokenInvalidError:
            raise ValidationError('invalid bot token!')
        finally:
            client.session.close()
            client.session.delete()
