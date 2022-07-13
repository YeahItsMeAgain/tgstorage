import asyncio
from typing import Union
from starlette import status
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException
from app.db import schemas

from app.db.crud.folder import FolderDAL
from app.db.crud.user import UserDAL
from app.db.models.shared_resource import EditorMethod
from app.db.schemas.user import SessionUser
from app.dependencies.auth import get_current_user, get_current_user_silent

router = APIRouter(prefix='/folders')

@cbv(router)
class Folders:
	user: SessionUser = Depends(get_current_user)

	@router.get("/root")
	async def root(self):
		db_user = await UserDAL.get_db_model_or_none(**self.user.dict())
		return await db_user.root_folder()

	@router.post("/{parent_uuid}/{folder_name}")
	async def create(self, parent_uuid: str, folder_name: str):
		db_parent = await FolderDAL.try_get_resource(uuid=parent_uuid, user=self.user, editors__in=[self.user.id])
		db_folder = await FolderDAL.get_db_or_create(
			schemas.CreateFolder(
				owner_id=db_parent.owner_id,
				creator_id=self.user.id,
				parent_id=db_parent.id,
				name=folder_name
			)
		)
		await db_folder.editors.add(*await db_parent.editors.all())

	@router.delete("/{uuid}")
	async def delete(self, uuid: str):
		return await FolderDAL.delete(editors=[self.user.id], uuid=uuid)

	@router.patch("/rename/{uuid}/{new_name}")
	async def rename(self, uuid: str, new_name: str):
		return await FolderDAL.update(editors=[self.user.id], uuid=uuid, name=new_name)

	@router.patch("/move/{source_uuid}/{target_uuid}")
	async def move(self, source_uuid: str, target_uuid: str):
		db_folder_source, db_folder_target = await asyncio.gather(
			FolderDAL.try_get_resource(uuid=source_uuid, user=self.user, editors__in=[self.user.id], is_root=False),
			FolderDAL.try_get_resource(uuid=target_uuid, user=self.user, editors__in=[self.user.id])
		)

		# Can be moved only if the source is not a root folder and the owners are the same.
		if db_folder_source.id != db_folder_target.id and \
			db_folder_source.owner_id == db_folder_target.owner_id:
			await FolderDAL.update_db_model(db_folder_source, parent_id=db_folder_target.id)

	@router.patch("/change_public_status/{is_public}/{uuid}")
	async def change_public_status(self, is_public: bool, uuid: str):
		return await FolderDAL.update_tree(owner_id=self.user.id, uuid=uuid, is_public=is_public)

	@router.patch("/editors/{method}/{uuid}/{editor_email}")
	async def change_editors(self, method: EditorMethod, uuid: str, editor_email: str):
		db_folder, db_user = await asyncio.gather(
			FolderDAL.get_db_model_or_none(uuid=uuid, owner_id=self.user.id),
			UserDAL.get_db_model_or_none(email=editor_email),
		)

		if not db_folder or not db_user or \
			(await db_folder.owner).email == editor_email :
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

		await FolderDAL.change_tree_editors(db_folder=db_folder, editor=db_user, method=method)


# Routes that don't depend on the user being logged in.
@cbv(router)
class AnonymousFolders:
	user_or_none: Union[SessionUser, None] = Depends(get_current_user_silent)

	@router.get("/{uuid}")
	async def get(self, uuid: str):
		return await schemas.ViewFolder.from_tortoise_orm(
			await FolderDAL.try_get_resource(uuid=uuid, user=self.user_or_none)
		)
