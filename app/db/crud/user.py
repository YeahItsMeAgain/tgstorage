from app.db import models, schemas

async def get_user(user_id: int):
    return await schemas.User.from_queryset_single(models.User.get(id=user_id))


async def get_user_by_email(email: str):
    return await schemas.User.from_queryset_single(models.User.get(email=email))


async def get_users(skip: int = 0, limit: int = 100):
    return await schemas.User.from_queryset(models.User.filter().offset(skip).limit(limit).all())

async def get_user_or_create(user: schemas.User):
    return await models.User.get_or_create(**user.dict(exclude_unset=True))

async def create_user(user: schemas.User):
    user = await models.User.create(**user.dict(exclude_unset=True))
    return await schemas.User.from_tortoise_orm(user)
