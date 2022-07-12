import asyncio
from tortoise.queryset import Q

from app.db import models, schemas


class ShareDAL:
	@staticmethod
	async def _get_folder_tree(db_folder: models.Folder, shared_user_email: str):
		shares = []
		async def share_folder_tree_inner(db_folder: models.Folder):
			nonlocal shares
			shares.extend(
				[
					models.SharedResource(
						owner_id=db_folder.owner_id,
						folder_id=db_folder.id,
						shared_user_email=shared_user_email
					)
				] +
				[
					models.SharedResource(
						owner_id=db_folder.owner_id,
						file_id=file_id,
						shared_user_email=shared_user_email
					)
					for file_id in await db_folder.files.all().values_list('id', flat=True)
				]
			)
			await asyncio.gather(*[
                share_folder_tree_inner(sub_folder)
                for sub_folder in await db_folder.sub_folders.all()
            ])

		await share_folder_tree_inner(db_folder)
		return shares

	@staticmethod
	async def share_folder_tree(db_folder: models.Folder, shared_user_email: str):
		await models.SharedResource.bulk_create(
			await ShareDAL._get_folder_tree(db_folder, shared_user_email)
		)

	@staticmethod
	async def unshare_folder_tree(db_folder: models.Folder, shared_user_email: str):
		folder_ids, file_ids = [], []
		for model in await ShareDAL._get_folder_tree(db_folder, shared_user_email):
			if model.folder_id:
				folder_ids.append(model.folder_id)
			elif model.file_id:
				file_ids.append(model.file_id)

		await models.SharedResource.filter(
			Q(shared_user_email=shared_user_email) &
			(Q(file_id__in=file_ids) | Q(folder_id__in=folder_ids))
		).delete()

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
