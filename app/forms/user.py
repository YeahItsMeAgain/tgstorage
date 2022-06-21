from starlette_wtf import StarletteForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired
from telethon.errors.rpcerrorlist import AccessTokenInvalidError

from app.dependencies.settings import get_settings
from app.dependencies.connect_bot import connect_bot

class GetUserBotTokenForm(StarletteForm):
    bot_token = StringField(
        'Bot Token',
        validators=[
            DataRequired('Please enter a valid bot token'),
        ]
    )

    async def async_validate_bot_token(self, bot_token, settings= get_settings()):
        try:
            self._request.session['bot_token'] = bot_token.data
            await connect_bot(self._request, settings)
        except AccessTokenInvalidError as exc:
            raise ValidationError('invalid bot token!') from exc
