from app.db import models, schemas

class FolderDAL:
	@staticmethod
	async def get_or_create(folder: schemas.FolderType) -> schemas.Folder:
		db_folder, _ = await models.Folder.get_or_create(**folder.dict())
		return await schemas.Folder.from_tortoise_orm(db_folder)

	@staticmethod
	async def get_or_none(owner: int, uuid: str):
		db_folder = await models.Folder.get_or_none(owner=owner, uuid=uuid)
		if db_folder is None:
			return None

		return await schemas.Folder.from_tortoise_orm(db_folder)

	@staticmethod
	async def delete(owner: int, uuid: str):
		return await models.Folder.filter(owner=owner, uuid=uuid).delete()

	@staticmethod
	async def update(owner: int, uuid: str, **kwargs):
		return await models.Folder.filter(owner=owner, uuid=uuid).update(**kwargs)