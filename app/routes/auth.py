from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_restful.cbv import cbv
from starlette.requests import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError

from app import oauth
from app.dependencies.auth import get_current_user_silent
from app.db.schemas.user import BasicUser
from app.db import schemas
from app.db.crud.user import UserDAL
from app.db.crud.folder import FolderDAL
from app.dependencies.settings import get_settings
from app.routes.user import User
from app.settings import Settings

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={404: {"description": "Not found"}}
)


@cbv(router)
class Auth:
    user: BasicUser = Depends(get_current_user_silent)
    settings: Settings = Depends(get_settings)

    @router.get('/google')
    async def auth_via_google(self, request: Request):
        if self.user:
            return RedirectResponse(url='/')

        try:
            token = await oauth.google.authorize_access_token(request)
            user = token.get('userinfo')

            if not user.email or not user.email_verified or \
                    (len(self.settings.ALLOWED_MAILS) and user.email not in self.settings.ALLOWED_MAILS):
                raise OAuthError

            db_user = await UserDAL.get_or_create(
                schemas.BasicUser(
                    name=user.name, email=user.email
                )
            )
            await FolderDAL.get_or_create(
                schemas.CreateFolder(
                    owner_id=db_user.id, is_root=True, name='/'
                )
            )
            request.session['name'] = db_user.name
            request.session['email'] = db_user.email

            return RedirectResponse(request.url_for(User.setup.__name__))
        except OAuthError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='login failed')

    @router.get('/login/google')
    async def login_via_google(self, request: Request):
        if self.user:
            return RedirectResponse(url='/')

        request.session.clear()
        return await oauth.google.authorize_redirect(
            request,
            request.url_for(self.auth_via_google.__name__)
        )

    @router.get('/logout')
    async def logout(self, request: Request):
        request.session.pop('name', None)
        request.session.pop('email', None)
        return RedirectResponse(url='/')
