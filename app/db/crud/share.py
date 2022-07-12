from app.db import models, schemas


class ShareDAL:
	@staticmethod
	async def get_db_or_create(share: schemas.ShareType):
		db_share, _ = await models.SharedResource.get_or_create(**share.dict())
		return db_share

	@staticmethod
	async def get_by_filter(**kwargs):
		return await schemas.ViewShare.from_queryset(
			models.SharedResource.filter(**kwargs).all()
		)

	@staticmethod
	async def delete(owner: int, shared_user_email: str, **kwargs):
		return await models.SharedResource.filter(
			owner=owner, shared_user_email=shared_user_email, **kwargs
		).delete()
