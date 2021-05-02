from fastapi import APIRouter, status
from fastapi_restful.cbv import cbv
from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse
from starlette_wtf import csrf_protect
from jinja2 import Template

from app.forms.user import GetDataForm

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
class Auth:
	@router.api_route('/data', methods=['GET', 'POST'])
	@csrf_protect
	async def get_data(self, request: Request):
		# initialize form
		form = await GetDataForm.from_formdata(request)

		# validate form
		if await form.validate_on_submit():
			return RedirectResponse(url='/', status_code=status.HTTP_301_MOVED_PERMANENTLY)

		# generate html
		html = template.render(form=form)

		# return response
		status_code = status.HTTP_402_PAYMENT_REQUIRED if form.errors else status.HTTP_200_OK
		return HTMLResponse(html, status_code=status_code)