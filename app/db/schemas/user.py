from tortoise.contrib.pydantic import pydantic_model_creator

from app.db.models import User as UserModel

User = pydantic_model_creator(UserModel, name=UserModel.__name__)
