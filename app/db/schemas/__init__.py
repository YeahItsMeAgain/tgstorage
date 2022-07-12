# https://tortoise-orm.readthedocs.io/en/latest/contrib/pydantic.html?highlight=Early#relations-early-init
from tortoise import Tortoise
Tortoise.init_models(["app.db.models"], "models")
 
from .user import CreateUser, SessionUser, UserType
from .folder import ViewFolder, CreateFolder, FolderType
from .file import ViewFile, CreateFile, FileType
from .share import ViewShare, CreateShare, ShareType

__all__ = [
    'UserType',
    'FolderType',
    'FileType',
    'ShareType',
    CreateUser.__name__,
    SessionUser.__name__,
    ViewFolder.__name__,
    CreateFolder.__name__,
    ViewFile.__name__,
    CreateFile.__name__,
    ViewShare.__name__,
    CreateShare.__name__,
]
