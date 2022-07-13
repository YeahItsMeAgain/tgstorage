from fastapi import APIRouter, status, Depends
from fastapi_restful.cbv import cbv
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette_wtf import csrf_protect
from jinja2 import Template

from app.dependencies.auth import get_current_user
from app.db.crud.user import UserDAL
from app.forms.user import GetUserBotForm
from app.db.schemas.user import SessionUser

# TODO: move this to frontend
template = Template('''
<html>
	<body>
	<h1>Connect Bot</h1>
	<form method="post" novalidate>
		{{ form.csrf_token }}
		<div>
		{{ form.bot_token(placeholder='Bot token',
						autofocus='true') }}
		{% if form.bot_token.errors -%}
		<span>{{ form.bot_token.errors[0] }}</span>
		{%- endif %}
		{{ form.chat_id(placeholder='Chat id') }}
		{% if form.chat_id.errors -%}
		<span>{{ form.chat_id.errors[0] }}</span>
		{%- endif %}
		</div>
		<button type="submit">Connect Bot</button>
	</form>
	</body>
</html>
''')

router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {"description": "Not found"}}
)


@cbv(router)
class User:
    user: SessionUser = Depends(get_current_user)

    @router.get('/setup')
    async def setup(self, request: Request):
        db_user = await UserDAL.get_db_model_or_none(**self.user.dict())

        if not db_user.bot_token or not db_user.chat_id:
            return RedirectResponse(url=request.url_for(User.get_data.__name__))
        else:
            request.session['bot_token'] = db_user.bot_token
            request.session['chat_id'] = db_user.chat_id

        return RedirectResponse(url='/')

    @router.api_route('/data', methods=['GET', 'POST'])
    @csrf_protect
    async def get_data(self, request: Request):
        # initialize form
        form = await GetUserBotForm.from_formdata(request)

        # validate form
        if await form.validate_on_submit():
            await UserDAL.update(
                {'email': self.user.email},
                {
                    'bot_token': form.bot_token.data,
                    'chat_id': form.chat_id.data
                }
            )
            request.session['bot_token'] = form.bot_token.data
            request.session['chat_id'] = form.chat_id.data
            return RedirectResponse(url='/')

        # generate html
        html = template.render(form=form)

        # return response
        status_code = status.HTTP_402_PAYMENT_REQUIRED if form.errors else status.HTTP_200_OK
        return HTMLResponse(html, status_code=status_code)
