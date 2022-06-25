from typing import Union

import pydantic

from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import User as UserModel

User = pydantic_model_creator(UserModel, name=UserModel.__name__)
BasicUser = pydantic_model_creator(
    UserModel, name=f'Basic{UserModel.__name__}',
    include=['name', 'email', 'chat_id']
)
BasicUser.Config.extra = pydantic.main.Extra.ignore
UserType = Union[BasicUser, User]
