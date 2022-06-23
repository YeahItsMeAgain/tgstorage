# https://tortoise-orm.readthedocs.io/en/latest/contrib/pydantic.html?highlight=Early#relations-early-init
from tortoise import Tortoise
Tortoise.init_models(["app.db.models"], "models")
 
from .user import BasicUser, User, UserType
from .folder import CreateFolder, Folder, FolderType


__all__ = [
    'UserType',
    'FolderType',
    BasicUser.__name__,
    User.__name__,
    Folder.__name__,
    CreateFolder.__name__
]
