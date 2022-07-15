from typing import Union
from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import File as FileModel

ViewFile = pydantic_model_creator(
    FileModel, name=f'View{FileModel.__name__}'
)

CreateFile = pydantic_model_creator(
    FileModel, name=f'Create{FileModel.__name__}',
    include=['name', 'owner_id', 'creator_id', 'folder_id', 'tg_message_id'],
    exclude=FileModel.PydanticMeta.optional + ['owner', 'creator', 'editors']
)

FileType = Union[ViewFile, CreateFile]
