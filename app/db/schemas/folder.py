import pydantic
from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import Folder as FolderModel

Folder = pydantic_model_creator(FolderModel, name=FolderModel.__name__)

class CreateFolder(pydantic.BaseModel):
    owner_id: int
    name: str
    is_root: bool
    class Config:
        orm_mode = True
        orig_model = FolderModel
