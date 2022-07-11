# https://tortoise-orm.readthedocs.io/en/latest/contrib/pydantic.html?highlight=Early#relations-early-init
from tortoise import Tortoise
Tortoise.init_models(["app.db.models"], "models")
 
from .user import CreateUser, SessionUser, User, UserType
from .folder import CreateFolder, Folder, FolderType
from .file import CreateFile, File, FileType

__all__ = [
    'UserType',
    'FolderType',
    'FileType',
    CreateUser.__name__,
    SessionUser.__name__,
    User.__name__,
    Folder.__name__,
    CreateFolder.__name__,
    File.__name__,
    CreateFile.__name__,
]
