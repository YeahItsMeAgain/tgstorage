from pydantic import BaseModel
from tortoise.models import Model

class DAL:
	model: Model

	@classmethod
	async def get_db_or_create(cls, model: BaseModel):
		db_obj, _ = await cls.model.get_or_create(**model.dict())
		return db_obj

	@classmethod
	async def get_db_model_or_none(cls, **kwargs):
		return await cls.model.get_or_none(**kwargs)

	@classmethod
	async def update(cls, filter_args: dict, update_args: dict):
		await cls.model.select_for_update().filter(**filter_args).update(**update_args)
		return True

	@staticmethod
	async def update_db_model(db_obj: Model, **kwargs):
		await db_obj.update_from_dict(kwargs).save(update_fields=kwargs.keys())
		return True

	@classmethod
	async def delete(cls, **kwargs):
		db_obj = await cls.get_db_model_or_none(**kwargs)
		if not db_obj:
			return False

		await db_obj.delete()
		return True
