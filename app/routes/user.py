from fastapi import APIRouter, status, Depends
from fastapi_restful.cbv import cbv
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette_wtf import csrf_protect
from jinja2 import Template

from app.dependencies.auth import get_current_user
from app.db.crud.user import UserDAL
from app.forms.user import GetUserBotTokenForm
from app.db.schemas.user import BasicUser

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
    user: BasicUser = Depends(get_current_user)

    @router.get('/setup')
    async def setup(self, request: Request):
        db_user = await UserDAL.get_or_none(
            BasicUser(
                name=self.user.name, email=self.user.email
            )
        )

        if not db_user.bot_token:
            return RedirectResponse(url=request.url_for(User.get_data.__name__))

        return RedirectResponse(url='/')


    @router.api_route('/data', methods=['GET', 'POST'])
    @csrf_protect
    async def get_data(self, request: Request):
        # initialize form
        form = await GetUserBotTokenForm.from_formdata(request)

        # validate form
        if await form.validate_on_submit():
            await UserDAL.update({'email': self.user.email}, {'bot_token': form.bot_token.data})
            return RedirectResponse(url='/')

        # generate html
        html = template.render(form=form)

        # return response
        status_code = status.HTTP_402_PAYMENT_REQUIRED if form.errors else status.HTTP_200_OK
        return HTMLResponse(html, status_code=status_code)
