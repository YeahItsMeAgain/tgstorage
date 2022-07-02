from starlette import status
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException
from app.db import schemas

from app.db.crud.folder import FolderDAL
from app.db.crud.user import UserDAL
from app.db.schemas.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(
	prefix='/folders',
	tags=['folders'],
	responses={404: {"description": "Not found"}}
)


@cbv(router)
class Folders:
	user: User = Depends(get_current_user)

	@router.get("/root")
	async def root(self):
		db_user = await UserDAL.get_db_model_or_none(self.user)
		return await db_user.root_folder()

	@router.get("/{uuid}")
	async def get(self, uuid: str):
		return await FolderDAL.get_or_none(self.user.id, uuid)

	@router.post("/{parent_uuid}/{folder_name}")
	async def create(self, parent_uuid: str, folder_name: str):
		parent = await FolderDAL.get_or_none(self.user.id, parent_uuid)
		if not parent:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'parent {parent_uuid} does not exist'
			)

		await FolderDAL.get_or_create(
			schemas.CreateFolder(
				owner_id=self.user.id,
				parent_id=parent.id,
				name=folder_name
			)
		)

	@router.delete("/{uuid}")
	async def delete(self, uuid: str):
		deleted_count = await FolderDAL.delete(self.user.id, uuid)
		if not deleted_count:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'folder {uuid} does not exist'
			)

	@router.patch("/rename/{uuid}/{new_name}")
	async def rename(self, uuid: str, new_name: str):
		updated_count = await FolderDAL.update(self.user.id, uuid=uuid, name=new_name)
		if not updated_count:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'folder {uuid} does not exist'
			)