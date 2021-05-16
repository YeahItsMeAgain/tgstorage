import pydantic
from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import User as UserModel

# TODO: use https://github.com/tortoise/tortoise-orm/pull/770 when is merged
User = pydantic_model_creator(UserModel, name=UserModel.__name__)
BasicUser = pydantic_model_creator(
    UserModel, name=f'Basic{UserModel.__name__}',
    include=['username', 'email'],
)
BasicUser.Config.extra = pydantic.main.Extra.ignore

CreateUser = pydantic_model_creator(
    UserModel, name=f'Create{UserModel.__name__}',
    exclude=['id', 'created_at', 'modified_at'],
    optional=['bot_token']
)
