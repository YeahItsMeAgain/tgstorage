from fastapi import Request
from fastapi.exceptions import HTTPException
from starlette import status

from app.db.schemas.user import SessionUser


def _get_current_user(request: Request, silent) -> SessionUser:
    id = request.session.get('id', None)
    name = request.session.get('name', None)
    email = request.session.get('email', None)
    chat_id = request.session.get('chat_id', None)

    if not id or not name or not email:
        if silent:
            return None

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="login required",
        )

    return SessionUser(id=id, name=name, email=email, chat_id=chat_id)


def get_current_user(request: Request) -> SessionUser:
    return _get_current_user(request, False)

def get_current_user_silent(request: Request) -> SessionUser:
    return _get_current_user(request, True)
