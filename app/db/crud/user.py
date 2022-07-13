from app.db import models, schemas

class UserDAL:
    @staticmethod
    async def get_db_or_create(user: schemas.UserType) -> models.User:
        db_user, _  = await models.User.get_or_create(**user.dict())
        return db_user

    @staticmethod
    async def get_db_model_or_none(**kwargs) -> models.User:
        return await models.User.get_or_none(**kwargs)

    @staticmethod
    async def update(filter_args: dict, update_args: dict):
        await models.User.select_for_update().filter(**filter_args).update(**update_args)
