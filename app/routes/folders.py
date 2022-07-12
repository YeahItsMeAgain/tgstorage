from starlette import status
from fastapi_restful.cbv import cbv
from fastapi import APIRouter, Depends, HTTPException, Request
from app.db import schemas

from app.db.crud.folder import FolderDAL
from app.db.crud.user import UserDAL
from app.db.schemas.user import SessionUser
from app.dependencies.auth import get_current_user

router = APIRouter(
	prefix='/folders',
	tags=['folders'],
	responses={404: {"description": "Not found"}}
)


@cbv(router)
class Folders:
	user: SessionUser = Depends(get_current_user)

	@staticmethod
	async def try_get_folder(owner_id: int, uuid: str):
		db_folder = await FolderDAL.get_db_model_or_none(owner_id=owner_id, uuid=uuid)
		if not db_folder:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'folder {uuid} does not exist'
			)
		return db_folder

	@router.get("/root")
	async def root(self):
		db_user = await UserDAL.get_db_model_or_none(self.user)
		return await db_user.root_folder()

	@router.post("/{parent_uuid}/{folder_name}")
	async def create(self, parent_uuid: str, folder_name: str):
		db_folder = await Folders.try_get_folder(self.user.id, parent_uuid)
		await FolderDAL.get_db_or_create(
			schemas.CreateFolder(
				owner_id=self.user.id,
				parent_id=db_folder.id,
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

	@router.patch("/change_public_status/{is_public}/{uuid}")
	async def change_public_status(self, is_public: bool, uuid: str):
		await FolderDAL.update_tree(owner=self.user.id, uuid=uuid, is_public=is_public)

# Routes that don't depend on the user being logged in.
@router.get("/{uuid}")
async def get(uuid: str, request: Request):
	db_folder = await FolderDAL.get_db_model_or_none(uuid)
	if not db_folder:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f'folder {uuid} does not exist'
		)

	try:
		current_user = get_current_user(request)
		current_user_id = current_user.id
		current_user_email = current_user.email
	except:
		current_user_id = None
		current_user_email = None

	if (current_user_id and db_folder.owner_id == current_user_id) or \
			await FolderDAL.is_public_or_shared(uuid, current_user_email):
		return await schemas.ViewFolder.from_tortoise_orm(db_folder)
