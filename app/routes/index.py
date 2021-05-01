from typing import Dict
from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from starlette.requests import Request

from app.dependencies.auth import get_current_user

router = APIRouter(
	prefix='/index',
	tags=['index'],
	responses={404: {"description": "Not found"}}
)

@cbv(router)
class Index:
	user: Dict = Depends(get_current_user)

	@router.get('/')
	async def index(self, _: Request):
		return self.user, "index"
