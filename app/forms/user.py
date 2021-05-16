from starlette_wtf import StarletteForm
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import AccessTokenInvalidError
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
import uuid

from app import API_ID, API_HASH

class GetUserBotTokenForm(StarletteForm):
    bot_token = StringField(
        'Bot Token',
        validators=[
            DataRequired('Please enter a valid bot token'),
        ]
    )

    async def async_validate_bot_token(self, bot_token):
        client = TelegramClient(str(uuid.uuid4()), API_ID, API_HASH)
        try:
            await client.start(bot_token=bot_token.data)
            await client.log_out()
        except AccessTokenInvalidError:
            raise ValidationError('invalid bot token!')
        finally:
            client.session.close()
            client.session.delete()
