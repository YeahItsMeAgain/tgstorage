from typing import Union
from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from telethon import TelegramClient
from starlette.requests import Request
from fastapi_restful.cbv import cbv
from fastapi.responses import StreamingResponse

from app import fast_telethon
from app.db import schemas
from app.db.crud.file import FileDAL
from app.dependencies.auth import get_current_user, get_current_user_silent
from app.dependencies.chat import get_current_chat
from app.dependencies.connect_bot import connect_bot, get_bot
from app.dependencies.settings import get_settings
from app.routes.folders import Folders

router = APIRouter(
	prefix='/files',
	tags=['files'],
	responses={404: {"description": "Not found"}}
)


@cbv(router)
class Files:
	bot: TelegramClient = Depends(connect_bot)
	chat: int = Depends(get_current_chat)
	user: schemas.SessionUser = Depends(get_current_user)

	@staticmethod
	async def try_get_file(uuid: str, user: Union[schemas.SessionUser, None], **kwargs):
		db_file = await FileDAL.get_db_model_or_none(uuid=uuid, **kwargs)

		current_user_id = getattr(user, 'id', None)
		current_user_email = getattr(user, 'email', None)

		if db_file and \
			(
				db_file.is_public or \
				(current_user_id and db_file.owner_id == current_user_id) or \
				(current_user_email and await db_file.shares.filter(shared_user_email=current_user_email).exists())
			):
			return db_file

		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f'file {uuid} does not exist'
		)


	@router.patch("/rename/{uuid}/{new_name}")
	async def rename(self, uuid: str, new_name: str):
		updated_count = await FileDAL.update(self.user.id, uuid=uuid, name=new_name)
		if not updated_count:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'file {uuid} does not exist'
			)

	@router.patch("/change_public_status/{is_public}/{uuid}")
	async def change_public_status(self, is_public: bool, uuid: str):
		await FileDAL.update(self.user.id, uuid, is_public=is_public)

	@router.delete("/{uuid}")
	async def delete(self, uuid: str):
		deleted_count = await FileDAL.delete(self.user.id, uuid)
		if not deleted_count:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'file {uuid} does not exist'
			)

	@router.post("/upload/{folder_uuid}/{file_name}")
	async def create_file(self, folder_uuid: str, file_name: str, request: Request):
		def progress_callback(current, total):
			print(f'{current * 100 / total}%')

		folder = await Folders.try_get_folder(folder_uuid, self.user, owner_id=self.user.id)
		if await folder.files.filter(name=file_name).exists():
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'file {file_name} already exists'
			)

		message = await self.bot.send_file(
			self.chat,
			await fast_telethon.upload_from_request(self.bot, request, file_name, progress_callback)
		)

		await FileDAL.get_db_or_create(schemas.CreateFile(
			name=file_name,
			owner_id=self.user.id,
			folder_id=folder.id,
			tg_message_id=message.id
		))

# Routes that don't depend on the user being logged in.
@router.get("/{uuid}")
async def get(uuid: str, request: Request):
	return await schemas.ViewFile.from_tortoise_orm(
		await Files.try_get_file(
			uuid,
			get_current_user_silent(request)
		)
	)

@router.get("/download/{uuid}")
async def download_file(uuid: str, request: Request):
	db_file = await Files.try_get_file(
		uuid,
		get_current_user_silent(request)
	)
	owner = await db_file.owner
	bot = await get_bot(owner.bot_token, owner.email, get_settings())
	message = await bot.get_messages(owner.chat_id, ids=db_file.tg_message_id)
	return StreamingResponse(
		fast_telethon.iter_download(bot, message.document)
	)
