from fastapi import Request
from fastapi.exceptions import HTTPException
from starlette import status

from app.db.schemas.user import BasicUser


def _get_current_user(request: Request, silent) -> BasicUser:
    name = request.session.get('name', None)
    email = request.session.get('email', None)

    if not name or not email:
        if silent:
            return None

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="login required",
        )

    return BasicUser(name=name, email=email)


def get_current_user(request: Request) -> BasicUser:
    return _get_current_user(request, False)

def get_current_user_silent(request: Request) -> BasicUser:
    return _get_current_user(request, True)
