import asyncio
from typing import List, Union

from app.db import models, schemas
from app.db.models.shared_resource import EditorMethod


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
	async def delete(editors: List[int], uuid: str):
		db_folder = await FolderDAL.get_db_model_or_none(uuid, editors__in=editors)
		if not db_folder:
			return False
		await db_folder.delete()
		return True

	@staticmethod
	async def update_db_model(db_folder: models.Folder, **kwargs):
		await db_folder.update_from_dict(kwargs).save(update_fields=kwargs.keys())
		return True

	@staticmethod
	async def update(editors: List[int], uuid: str, **kwargs):
		db_folder = await FolderDAL.get_db_model_or_none(uuid, editors__in=editors)
		if not db_folder:
			return False
		return await FolderDAL.update_db_model(db_folder, **kwargs)

	@staticmethod
	async def update_tree(owner_id: int, uuid: str, **kwargs):
		db_folder = await FolderDAL.get_db_model_or_none(uuid, owner_id=owner_id)
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
			models.Folder.bulk_update(objects, kwargs.keys())
			for objects in [folders, files] if objects
		])

	@staticmethod
	async def change_tree_editors(db_folder: models.Folder, editor: models.User, method=EditorMethod):
		tasks = []
		async def update_tree_inner(db_folder: models.Folder):
			nonlocal tasks
			tasks.extend(
				[getattr(db_folder.editors, method.value)(editor)] +
				[
					getattr(db_file.editors, method.value)(editor)
					for db_file in await db_folder.files.all()
				]
			)
			await asyncio.gather(*[
				update_tree_inner(sub_folder)
				for sub_folder in await db_folder.sub_folders.all()
			])
		await update_tree_inner(db_folder)
		await asyncio.gather(*tasks)
