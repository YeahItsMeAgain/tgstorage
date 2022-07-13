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

router = APIRouter(
	prefix='/folders',
	tags=['folders'],
	responses={404: {"description": "Not found"}}
)


@cbv(router)
class Folders:
	user: SessionUser = Depends(get_current_user)

	@staticmethod
	async def try_get_folder(uuid: str, user: Union[schemas.SessionUser, None], **kwargs):
		db_folder = await FolderDAL.get_db_model_or_none(uuid=uuid, **kwargs)

		current_user_id = getattr(user, 'id', None)
		current_user_email = getattr(user, 'email', None)

		if db_folder and \
			(
				(current_user_id and (await db_folder.editors.filter(id=current_user_id).exists())) or \
				await FolderDAL.is_public_or_shared(uuid, current_user_email)
			):
			return db_folder

		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f'folder {uuid} does not exist'
		)

	@router.get("/root")
	async def root(self):
		db_user = await UserDAL.get_db_model_or_none(**self.user.dict())
		return await db_user.root_folder()

	@router.post("/{parent_uuid}/{folder_name}")
	async def create(self, parent_uuid: str, folder_name: str):
		db_parent = await Folders.try_get_folder(parent_uuid, self.user, editors__in=[self.user.id])
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
		return await FolderDAL.delete([self.user.id], uuid)

	@router.patch("/rename/{uuid}/{new_name}")
	async def rename(self, uuid: str, new_name: str):
		return await FolderDAL.update([self.user.id], uuid=uuid, name=new_name)

	@router.patch("/change_public_status/{is_public}/{uuid}")
	async def change_public_status(self, is_public: bool, uuid: str):
		return await FolderDAL.update_tree(owner_id=self.user.id, uuid=uuid, is_public=is_public)

	@router.patch("/editors/{method}/{uuid}/{editor_email}")
	async def change_editors(self, method: EditorMethod, uuid: str, editor_email: str):
		db_folder, db_user = await asyncio.gather(
			FolderDAL.get_db_model_or_none(uuid, owner_id=self.user.id),
			UserDAL.get_db_model_or_none(email=editor_email),
		)

		if not db_folder or not db_user or \
			(await db_folder.owner).email == editor_email :
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

		await FolderDAL.change_tree_editors(db_folder, db_user, method)


# Routes that don't depend on the user being logged in.
@cbv(router)
class AnonymousFolders:
	user_or_none: Union[SessionUser, None] = Depends(get_current_user_silent)

	@router.get("/{uuid}")
	async def get(self, uuid: str):
		return await schemas.ViewFolder.from_tortoise_orm(
			await Folders.try_get_folder(
				uuid, self.user_or_none
			)
		)
