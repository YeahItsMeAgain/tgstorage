from .files import router as files_router
from .folders import router as folder_router
from .auth import router as auth_router
from .index import router as index_router
from .user import router as user_router


routers = [
    files_router,
    folder_router,
    auth_router,
    index_router,
    user_router
]

__all__ = [
    'routers'
]
