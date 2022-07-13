from typing import List
from app.db import models, schemas

class FileDAL:
	@staticmethod
	async def get_db_or_create(file: schemas.FileType):
		db_file, _ = await models.File.get_or_create(**file.dict())
		return db_file

	@staticmethod
	async def get_db_model_or_none(uuid: str, **kwargs):
		return await models.File.get_or_none(uuid=uuid, **kwargs)

	@staticmethod
	async def get_or_none(editors: List[int], uuid: str):
		db_file = await FileDAL.get_db_model_or_none(editors__in=editors, uuid=uuid)
		if not db_file:
			return None

		return await schemas.ViewFile.from_tortoise_orm(db_file)

	@staticmethod
	async def delete(editors: List[int], uuid: str):
		db_file = await FileDAL.get_db_model_or_none(uuid, editors__in=editors)
		if db_file:
			await db_file.delete()
			return True
		return False

	@staticmethod
	async def update(editors: List[int], uuid: str, **kwargs):
		db_file = await FileDAL.get_db_model_or_none(uuid, editors__in=editors)
		if db_file:
			await db_file.update_from_dict(kwargs).save(update_fields=kwargs.keys())
			return True
		return False
