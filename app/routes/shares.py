from starlette import status
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException
from app.db import schemas

from app.db.crud.share import ShareDAL
from app.db.schemas.user import SessionUser
from app.dependencies.auth import get_current_user
from app.routes.folders import Folders

router = APIRouter(
	prefix='/shares',
	tags=['share'],
	responses={404: {"description": "Not found"}}
)


@cbv(router)
class Shares:
	user: SessionUser = Depends(get_current_user)

	@router.get("/folder/{uuid}")
	async def get(self, uuid: str):
		db_folder = await Folders.try_get_folder(self.user.id, uuid)
		return await ShareDAL.get_by_filter(
			owner_id=self.user.id,
			folder_id=db_folder.id,
		)

	@router.post("/folder/{should_share}/{uuid}/{shared_user_email}")
	async def share(self, should_share: bool, uuid: str, shared_user_email: str):
		db_folder = await Folders.try_get_folder(self.user.id, uuid)

		if should_share:
			await ShareDAL.get_db_or_create(
				schemas.CreateShare(
					owner_id=self.user.id,
					folder_id=db_folder.id,
					shared_user_email=shared_user_email
				)
			)
			return True

		deleted_count = await ShareDAL.delete(
			owner=self.user.id,
			shared_user_email=shared_user_email,
			folder=db_folder.id
		)
		if not deleted_count:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail='share does not exist'
			)
