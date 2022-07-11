from typing import Union
from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import File as FileModel

File = pydantic_model_creator(
    FileModel, name=FileModel.__name__, optional=['id']
)

CreateFile = pydantic_model_creator(
    FileModel, name=f'Create{FileModel.__name__}',
    include=['name', 'owner_id', 'folder_id', 'tg_message_id']
)

FileType = Union[File, CreateFile]
