from app.db import models, schemas

class FileDAL:
	@staticmethod
	async def get_or_create(file: schemas.FileType) -> schemas.Folder:
		db_file, _ = await models.File.get_or_create(**file.dict())
		return await schemas.File.from_tortoise_orm(db_file)

	@staticmethod
	async def get_db_model_or_none(owner: int, uuid: str):
		return await models.File.get_or_none(owner=owner, uuid=uuid)

	@staticmethod
	async def get_or_none(owner: int, uuid: str):
		db_file = await FileDAL.get_db_model_or_none(owner=owner, uuid=uuid)
		if db_file is None:
			return None

		return await schemas.File.from_tortoise_orm(db_file)

	@staticmethod
	async def delete(owner: int, uuid: str):
		return await models.File.filter(owner=owner, uuid=uuid).delete()

	@staticmethod
	async def update(owner: int, uuid: str, **kwargs):
		return await models.File.filter(owner=owner, uuid=uuid).update(**kwargs)