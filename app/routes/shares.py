from starlette import status
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException
from app.db import schemas

from app.db.crud.share import ShareDAL
from app.db.schemas.user import SessionUser
from app.dependencies.auth import get_current_user
from app.routes.files import Files
from app.routes.folders import Folders

router = APIRouter(
	prefix='/shares',
	tags=['share'],
	responses={404: {"description": "Not found"}}
)


@cbv(router)
class Shares:
	user: SessionUser = Depends(get_current_user)

	@router.get("/file/{uuid}")
	async def get_file(self, uuid: str):
		db_file = await Files.try_get_file(uuid, self.user, owner_id=self.user.id)
		return await ShareDAL.get_by_filter(
			owner_id=self.user.id,
			file_id=db_file.id,
		)

	@router.post("/file/{should_share}/{uuid}/{shared_user_email}")
	async def share_file(self, should_share: bool, uuid: str, shared_user_email: str):
		db_file = await Files.try_get_file(uuid, self.user, owner_id=self.user.id)

		if not should_share:
			return await ShareDAL.unshare_file(db_file, shared_user_email)

		return await ShareDAL.share_file(db_file, shared_user_email)

	@router.get("/folder/{uuid}")
	async def get_folder(self, uuid: str):
		db_folder = await Folders.try_get_folder(uuid, self.user, owner_id=self.user.id)
		return await ShareDAL.get_by_filter(
			owner_id=self.user.id,
			folder_id=db_folder.id,
		)

	@router.post("/folder/{should_share}/{uuid}/{shared_user_email}")
	async def share_folder(self, should_share: bool, uuid: str, shared_user_email: str):
		db_folder = await Folders.try_get_folder(uuid, self.user, owner_id=self.user.id)

		if not should_share:
			return await ShareDAL.unshare_folder_tree(db_folder, shared_user_email)

		return await ShareDAL.share_folder_tree(db_folder, shared_user_email)
