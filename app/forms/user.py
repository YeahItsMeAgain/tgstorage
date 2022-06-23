from starlette_wtf import StarletteForm
from wtforms import StringField, ValidationError, IntegerField
from wtforms.validators import DataRequired
from telethon.errors.rpcerrorlist import AccessTokenInvalidError, ChatAdminRequiredError

from app.dependencies.settings import get_settings
from app.dependencies.connect_bot import connect_bot

class GetUserBotForm(StarletteForm):
    bot_token = StringField(
        'Bot Token',
        validators=[
            DataRequired('Please enter a valid bot token'),
        ]
    )

    chat_id = IntegerField(
        'Chat id',
        validators=[
            DataRequired('Please enter a valid chat id'),
        ]
    )

    async def async_validate_bot_token(self, bot_token, settings= get_settings()):
        try:
            self._request.session['bot_token'] = bot_token.data
            await connect_bot(self._request, settings)
        except AccessTokenInvalidError as exc:
            del self._request.session['bot_token']
            raise ValidationError('invalid bot token!') from exc
        except:
            raise ValidationError('Can\'t connect bot!')

    
    async def async_validate_chat_id(self, chat_id, settings= get_settings()):
        # Assuming the bot token is already validated.
        bot = await connect_bot(self._request, settings)

        try:
            await bot.send_message(chat_id.data, 'Connected!')
        except ValueError:
            raise ValidationError('Can\'t find the chat!')
        except ChatAdminRequiredError:
            raise ValidationError('Add permission for sending messages!')
        except:
            raise ValidationError('Can\'t connect to chat!')


