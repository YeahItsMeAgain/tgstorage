from .file import router as files_router
from .folder import router as folder_router
from .auth import router as auth_router
from .user import router as user_router
from .share import router as shares_router


routers = [
    files_router,
    folder_router,
    auth_router,
    user_router,
    shares_router
]

__all__ = [
    'routers'
]
