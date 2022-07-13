from typing import List, Union
from starlette import status
from fastapi import HTTPException

from app.db import schemas
from app.db.crud.crud import DAL

class ResourceDAL(DAL):
	@classmethod
	async def try_get_resource(cls, uuid: str, user: Union[schemas.UserType, None], **kwargs):
		db_resource = await cls.get_db_model_or_none(uuid=uuid, **kwargs)

		current_user_id = getattr(user, 'id', None)
		current_user_email = getattr(user, 'email', None)

		if db_resource and \
			(
				db_resource.is_public or \
				(current_user_id and (await db_resource.editors.filter(id=current_user_id).exists())) or \
				(current_user_email and (await db_resource.shares.filter(shared_user_email=current_user_email).exists()))
			):
			return db_resource

		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f'{uuid} does not exist'
		)


	@classmethod
	async def delete(cls, editors: List[int], uuid: str):
		return await super(ResourceDAL, cls).delete(uuid=uuid, editors__in=editors)

	@classmethod
	async def update(cls, editors: List[int], uuid: str, **kwargs):
		db_obj = await cls.get_db_model_or_none(uuid=uuid, editors__in=editors)
		if not db_obj:
			return False
		return await cls.update_db_model(db_obj, **kwargs)
