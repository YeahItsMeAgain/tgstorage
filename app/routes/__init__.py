from .files import router as files_router
from .auth import router as auth_router


routers = [
    files_router,
    auth_router
]

__all__ = [
    'routers'
]
