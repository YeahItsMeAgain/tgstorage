from app.db import models, schemas

class FolderDAL:
    @staticmethod
    async def get_or_none(folder: schemas.Folder) -> schemas.Folder:
        db_folder, _ = await models.Folder.get_or_none(**folder.dict(exclude_unset=True))
        return await schemas.Folder.from_tortoise_orm(db_folder)
