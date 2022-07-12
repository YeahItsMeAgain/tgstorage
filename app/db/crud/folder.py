import asyncio
from typing import Union
from app.db import models, schemas


class FolderDAL:
	@staticmethod
	async def get_db_or_create(folder: schemas.FolderType):
		db_folder, _ = await models.Folder.get_or_create(**folder.dict())
		return db_folder

	@staticmethod
	async def get_db_model_or_none(uuid: str, **kwargs):
		return await models.Folder.get_or_none(uuid=uuid, **kwargs)

	@staticmethod
	async def is_public_or_shared(uuid: str, shared_user_email: Union[str, None]):
		db_folder = await FolderDAL.get_db_model_or_none(uuid)
		if not db_folder:
			return False

		if db_folder.is_public:
			return True

		if shared_user_email and \
				await db_folder.shares.filter(shared_user_email=shared_user_email).exists():
			return True

		return False

	@staticmethod
	async def delete(owner: int, uuid: str):
		return await models.Folder.filter(owner=owner, uuid=uuid).delete()

	@staticmethod
	async def update(owner: int, uuid: str, **kwargs):
		return await models.Folder.filter(owner=owner, uuid=uuid).update(**kwargs)

	@staticmethod
	async def update_tree(owner: int, uuid: str, **kwargs):
		db_folder = await FolderDAL.get_db_model_or_none(uuid, owner=owner)
		if not db_folder:
			return

		folders, files = [], []
		async def update_tree_inner(db_folder: models.Folder):
			nonlocal folders, files
			folders.append(models.Folder(id=db_folder.id, **kwargs))
			files.extend(
				[
					models.File(id=file_id, **kwargs)
					for file_id in await db_folder.files.all().values_list('id', flat=True)
				]
			)
			await asyncio.gather(*[
				update_tree_inner(sub_folder)
				for sub_folder in await db_folder.sub_folders.all()
			])
		await update_tree_inner(db_folder)
		await asyncio.gather(*[
			models.Folder.bulk_update(folders, kwargs.keys()),
			models.File.bulk_update(files, kwargs.keys())
		])
