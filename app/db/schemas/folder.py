from typing import Union
from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import Folder as FolderModel

Folder = pydantic_model_creator(
    FolderModel, name=FolderModel.__name__, optional=['id']
)

CreateFolder = pydantic_model_creator(
    FolderModel, name=f'Create{FolderModel.__name__}',
    include=['parent_id', 'owner_id', 'is_root', 'name']
)

FolderType = Union[Folder, CreateFolder]
