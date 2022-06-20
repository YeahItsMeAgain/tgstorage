from app.db import models, schemas

class UserDAL:
    @staticmethod
    async def get_by_id(user_id: int):
        return await schemas.User.from_queryset_single(models.User.get(id=user_id))

    @staticmethod
    async def get_by_email(email: str):
        return await schemas.User.from_queryset_single(models.User.get(email=email))

    @staticmethod
    async def get(skip: int = 0, limit: int = 100):
        return await schemas.User.from_queryset(models.User.filter().offset(skip).limit(limit).all())

    @staticmethod
    async def get_or_create(user: models.User) -> schemas.User:
        db_user, _ = await models.User.get_or_create(**user.dict())
        return await schemas.User.from_tortoise_orm(db_user)

    @staticmethod
    async def get_or_none(user: models.User) -> schemas.User:
        db_user = await models.User.get_or_none(**user.dict())
        if db_user is None:
            return None
        return await schemas.User.from_tortoise_orm(db_user)

    @staticmethod
    async def update(filter_args: dict, update_args: dict):
        await models.User.select_for_update().filter(**filter_args).update(**update_args)

    @staticmethod
    async def create(user: models.User):
        db_user = await models.User.create(**user.dict())
        return await schemas.User.from_tortoise_orm(db_user)
