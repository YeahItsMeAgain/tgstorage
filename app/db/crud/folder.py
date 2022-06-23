from app.db import models, schemas

class FolderDAL:
    @staticmethod
    async def get_or_create(folder: schemas.FolderType) -> schemas.Folder:
        db_folder, _ = await models.Folder.get_or_create(**folder.dict())
        return await schemas.Folder.from_tortoise_orm(db_folder)
