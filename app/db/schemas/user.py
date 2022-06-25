from typing import Union

import pydantic

from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import User as UserModel

User = pydantic_model_creator(
    UserModel, name=UserModel.__name__
)
CreateUser = pydantic_model_creator(
    UserModel, name=f'Create{UserModel.__name__}',
    include=['name', 'email']
)

SessionUser = pydantic_model_creator(
    UserModel, name=f'Session{UserModel.__name__}',
    include=['id', 'name', 'email', 'chat_id']
)
CreateUser.Config.extra = pydantic.main.Extra.ignore
UserType = Union[CreateUser, User, SessionUser]
