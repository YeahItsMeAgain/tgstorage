from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_restful.cbv import cbv
from starlette.requests import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError

from app import oauth
from app.dependencies.auth import get_current_user_silent
from app.db.schemas.user import BasicUser
from app.routes.user import User
from app.db import schemas
from app.db.crud.user import UserDAL

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {"description": "Not found"}}
)


@cbv(router)
class Auth:
    user: BasicUser = Depends(get_current_user_silent)

    @router.get('/google')
    async def auth_via_google(self, request: Request):
        if self.user:
            return RedirectResponse(url='/')

        try:
            token = await oauth.google.authorize_access_token(request)
            user = await oauth.google.parse_id_token(request, token)

            if not user.email or not user.email_verified:
                raise OAuthError

            db_user = await UserDAL.get_or_create(
                schemas.CreateUser(
                    username=user.name, email=user.email
                )
            )
            request.session['username'] = db_user.username
            request.session['email'] = db_user.email

            if not db_user.bot_token:
                return RedirectResponse(url=request.url_for(User.get_data.__name__))

            return RedirectResponse('/')
        except OAuthError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='login failed')

    @router.get('/login/google')
    async def login_via_google(self, request: Request):
        if self.user:
            return RedirectResponse(url='/')

        redirect_uri = request.url_for(self.auth_via_google.__name__)
        return await oauth.google.authorize_redirect(request, redirect_uri)

    @router.get('/logout')
    async def logout(self, request: Request):
        request.session.pop('username', None)
        request.session.pop('email', None)
        return RedirectResponse(url='/')
