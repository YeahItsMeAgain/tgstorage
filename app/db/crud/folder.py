from app.db import models, schemas
from app.db.schemas.folder import CreateFolder

class FolderDAL:
    @staticmethod
    async def get_or_create(folder: CreateFolder) -> schemas.Folder:
        db_folder, _ = await models.Folder.get_or_create(**folder.dict())
        return await schemas.Folder.from_tortoise_orm(db_folder)
