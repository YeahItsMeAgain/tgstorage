from fastapi import APIRouter, HTTPException, status
from fastapi_restful.cbv import cbv
from starlette.requests import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError

from app import oauth

router = APIRouter(
	prefix='/auth',
	tags=['auth'],
	responses={404: {"description": "Not found"}}
)

@cbv(router)
class Auth:
	@router.get('/google')
	async def auth_via_google(self, request: Request):
		try:
			token = await oauth.google.authorize_access_token(request)
			user = await oauth.google.parse_id_token(request, token)

			if not user.email or not user.email_verified:
				raise OAuthError

			"""
				TODO: 	• create some sort of a user object
 					  	• save in the db the user
						• add step for getting the bot token	
 					  	• create a dependency to get current user(with bot)
			"""
			request.session['user'] = dict(user)
			return user
		except OAuthError:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='login failed')

	@router.get('/login/google')
	async def login_via_google(self, request: Request):
		redirect_uri = request.url_for(self.auth_via_google.__name__)
		return await oauth.google.authorize_redirect(request, redirect_uri)

	@router.get('/logout')
	async def logout(self, request: Request):
		request.session.pop('user', None)
		return RedirectResponse(url='/')
