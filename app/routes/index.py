from typing import Dict
from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from starlette.requests import Request
from app.db.schemas.user import SessionUser

from app.dependencies.auth import get_current_user

router = APIRouter(prefix='/index')

@cbv(router)
class Index:
	user: SessionUser = Depends(get_current_user)

	@router.get('/')
	async def index(self, _: Request):
		return self.user, "index"
