import aioredis
from typing import List

from app.db import models, schemas
from app.db.crud.resource import ResourceDAL
from app.redis_prefix import RedisPrefix


class FileDAL(ResourceDAL):
	model = models.File

	@staticmethod
	async def get_or_none(editors: List[int], uuid: str):
		db_file = await FileDAL.get_db_model_or_none(editors__in=editors, uuid=uuid)
		if not db_file:
			return None

		return await schemas.ViewFile.from_tortoise_orm(db_file)

	@staticmethod
	def get_user_upload_redis_key(user_id: int):
		return f'{RedisPrefix.UPLOAD.value}{user_id}'

	@staticmethod
	def _get_file_upload_redis_key(user_id: int, folder_uuid: str, file_name: str):
		return f'{RedisPrefix.UPLOAD.value}{user_id}{folder_uuid}{file_name}'

	@staticmethod
	async def set_upload_status(redis: aioredis.Redis, user_id: int, folder_uuid: str, file_name: str, current: int, total: int):
		await redis.set(
			FileDAL._get_file_upload_redis_key(user_id, folder_uuid, file_name),
			round(current * 100 / total, 2)
		)

	@staticmethod
	async def get_upload_status(redis: aioredis.Redis, user_id: int, folder_uuid: str, file_name: str):
		return await redis.get(
			FileDAL._get_file_upload_redis_key(user_id, folder_uuid, file_name)
		)

	@staticmethod
	async def delete_upload_status(redis: aioredis.Redis, user_id: int, folder_uuid: str, file_name: str):
		await redis.delete(
			FileDAL._get_file_upload_redis_key(user_id, folder_uuid, file_name)
		)
