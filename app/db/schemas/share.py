from typing import Union
from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import SharedResource as ShareModel

ViewShare = pydantic_model_creator(
    ShareModel, name=f'View{ShareModel.__name__}',
    include=['shared_user_email']
)

CreateShare = pydantic_model_creator(
    ShareModel, name=f'Create{ShareModel.__name__}',
    include=['owner_id', 'shared_user_email', 'folder_id', 'file_id'],
    optional=['folder_id', 'file_id']
)

ShareType = Union[ViewShare, CreateShare]
