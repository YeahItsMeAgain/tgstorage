from app.db import models
from app.db.crud.crud import DAL

class UserDAL(DAL):
	model = models.User

	@staticmethod
	async def update(filter_args: dict, update_args: dict):
		await super(UserDAL, UserDAL).update(filter_args, update_args)
