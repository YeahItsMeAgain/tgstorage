from .files import router as files_router
from .auth import router as auth_router
from .index import router as index_router


routers = [
    files_router,
    auth_router,
    index_router
]

__all__ = [
    'routers'
]
