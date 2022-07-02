from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import File as FileModel

File = pydantic_model_creator(
    FileModel, name=FileModel.__name__, optional=['id']
)
