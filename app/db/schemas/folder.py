from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import Folder as FolderModel

Folder = pydantic_model_creator(FolderModel, name=FolderModel.__name__)