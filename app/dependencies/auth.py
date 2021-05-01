from fastapi import Request
from fastapi.exceptions import HTTPException
from starlette import status


async def get_current_user(request: Request):
    user = request.session.get('user', None)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="login required",
        )

    return user
