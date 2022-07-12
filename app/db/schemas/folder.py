from typing import Union
from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import Folder as FolderModel

ViewFolder = pydantic_model_creator(
    FolderModel, name=f'View{FolderModel.__name__}',
    include=[
        'name', 'uuid', 'is_public',
        'files', 'sub_folders'
    ],
)

CreateFolder = pydantic_model_creator(
    FolderModel, name=f'Create{FolderModel.__name__}',
    include=['parent_id', 'owner_id', 'is_root', 'name'],
    exclude=FolderModel.PydanticMeta.optional
)

FolderType = Union[ViewFolder, CreateFolder]
