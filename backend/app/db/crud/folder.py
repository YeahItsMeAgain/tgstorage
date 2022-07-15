import asyncio

from app.db import models
from app.db.crud.resource import ResourceDAL
from app.db.models.shared_resource import EditorMethod


class FolderDAL(ResourceDAL):
	model = models.Folder

	@staticmethod
	async def update_tree(owner_id: int, uuid: str, **kwargs):
		db_folder = await FolderDAL.get_db_model_or_none(uuid=uuid, owner_id=owner_id)
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

		await asyncio.gather(*filter(None, [
			models.Folder.bulk_update(folders, kwargs.keys()) if folders else None,
			models.File.bulk_update(files, kwargs.keys()) if files else None
		]))

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
