from typing import List
from app.db import models, schemas
from app.db.crud.resource import ResourceDAL

class FileDAL(ResourceDAL):
	model = models.File

	@staticmethod
	async def get_or_none(editors: List[int], uuid: str):
		db_file = await FileDAL.get_db_model_or_none(editors__in=editors, uuid=uuid)
		if not db_file:
			return None

		return await schemas.ViewFile.from_tortoise_orm(db_file)
