from app.db import models, schemas

class UserDAL:
    @staticmethod
    async def get_or_create(user: schemas.UserType) -> schemas.User:
        db_user, _ = await models.User.get_or_create(**user.dict())
        return await schemas.User.from_tortoise_orm(db_user)

    @staticmethod
    async def get_or_none(user: schemas.UserType) -> schemas.User:
        db_user = await models.User.get_or_none(**user.dict())
        if db_user is None:
            return None
        return await schemas.User.from_tortoise_orm(db_user)

    @staticmethod
    async def update(filter_args: dict, update_args: dict):
        await models.User.select_for_update().filter(**filter_args).update(**update_args)
