import asyncio
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
from app.db.crud.user import UserDAL
from app.db.models.shared_resource import EditorMethod
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
				(current_user_id and (await db_file.editors.filter(id=current_user_id).exists())) or \
				(current_user_email and (await db_file.shares.filter(shared_user_email=current_user_email).exists()))
			):
			return db_file

		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=f'file {uuid} does not exist'
		)


	@router.patch("/rename/{uuid}/{new_name}")
	async def rename(self, uuid: str, new_name: str):
		return await FileDAL.update(editors=[self.user.id], uuid=uuid, name=new_name)

	@router.patch("/change_public_status/{is_public}/{uuid}")
	async def change_public_status(self, is_public: bool, uuid: str):
		return await FileDAL.update([self.user.id], uuid, is_public=is_public)

	@router.patch("/editors/{method}/{uuid}/{editor_email}")
	async def add_editor(self, method: EditorMethod, uuid: str, editor_email: str):
		db_file, db_user = await asyncio.gather(
			FileDAL.get_db_model_or_none(uuid, owner_id=self.user.id),
			UserDAL.get_db_model_or_none(email=editor_email),
		)

		if not db_file or not db_user or \
			(await db_file.owner).email == editor_email :
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
		await getattr(db_file.editors, method.value)(db_user)
		return True

	@router.patch("/move/{file_uuid}/{folder_uuid}")
	async def move(self, file_uuid: str, folder_uuid: str):
		db_file_source, db_folder_target = await asyncio.gather(
			Files.try_get_file(file_uuid, self.user, editors__in=[self.user.id]),
			Folders.try_get_folder(folder_uuid, self.user, editors__in=[self.user.id])
		)

		# Can be moved only if the owners are the same.
		if db_file_source.owner_id == db_folder_target.owner_id:
			return await FileDAL.update_db_model(db_file_source, folder_id=db_folder_target.id)

	@router.delete("/{uuid}")
	async def delete(self, uuid: str):
		return await FileDAL.delete([self.user.id], uuid)

	@router.post("/upload/{folder_uuid}/{file_name}")
	async def create_file(self, folder_uuid: str, file_name: str, request: Request):
		def progress_callback(current, total):
			print(f'{current * 100 / total}%')

		db_folder = await Folders.try_get_folder(folder_uuid, self.user, editors__in=[self.user.id])
		if await db_folder.files.filter(name=file_name).exists():
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'file {file_name} already exists'
			)

		message = await self.bot.send_file(
			self.chat,
			await fast_telethon.upload_from_request(self.bot, request, file_name, progress_callback)
		)

		db_file = await FileDAL.get_db_or_create(
			schemas.CreateFile(
				name=file_name,
				owner_id=db_folder.owner_id,
				creator_id=self.user.id,
				folder_id=db_folder.id,
				tg_message_id=message.id
			)
		)
		await db_file.editors.add(*await db_folder.editors.all())
		return True


# Routes that don't depend on the user being logged in.
@cbv(router)
class AnonymousFiles:
	user_or_none: Union[schemas.SessionUser, None] = Depends(get_current_user_silent)

	@router.get("/{uuid}")
	async def get(self, uuid: str):
		return await schemas.ViewFile.from_tortoise_orm(
			await Files.try_get_file(uuid, self.user_or_none)
		)

	@router.get("/download/{uuid}")
	async def download_file(self, uuid: str):
		db_file = await Files.try_get_file(uuid, self.user_or_none)
		creator = await db_file.creator
		bot = await get_bot(creator.bot_token, creator.email, get_settings())
		message = await bot.get_messages(creator.chat_id, ids=db_file.tg_message_id)
		return StreamingResponse(
			fast_telethon.iter_download(bot, message.document),
			headers={'Content-Disposition': f'filename={db_file.name}'}
		)
