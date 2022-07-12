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
        async def recursive_check(folder: models.Folder, shared_user_email: Union[str, None]):
            if not folder:
                return False
            if folder.is_public:
                return True
            if shared_user_email and \
                    await folder.shares.filter(shared_user_email=shared_user_email).exists():
                return True

            return await recursive_check(await folder.parent, shared_user_email)
        return await recursive_check(await models.Folder.get_or_none(uuid=uuid), shared_user_email)

    @staticmethod
    async def delete(owner: int, uuid: str):
        return await models.Folder.filter(owner=owner, uuid=uuid).delete()

    @staticmethod
    async def update(owner: int, uuid: str, **kwargs):
        return await models.Folder.filter(owner=owner, uuid=uuid).update(**kwargs)
