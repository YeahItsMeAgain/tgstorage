from types import FunctionType
from typing import Dict
from fastapi import status, Request
from starlette.responses import RedirectResponse

from app.routes.auth import Auth

async def login_required(request: Request, _):
    return RedirectResponse(url=request.url_for(Auth.login_via_google.__name__))

exceptions_handlers: Dict[str, FunctionType] = {
    status.HTTP_401_UNAUTHORIZED: login_required
}
