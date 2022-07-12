from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from telethon import TelegramClient
from starlette.requests import Request
from fastapi_restful.cbv import cbv
from fastapi.responses import StreamingResponse

from app import fast_telethon
from app.db import schemas
from app.db.crud.file import FileDAL
from app.db.crud.folder import FolderDAL
from app.dependencies.auth import get_current_user
from app.dependencies.chat import get_current_chat
from app.dependencies.connect_bot import connect_bot

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

	@router.get("/{uuid}")
	async def get(self, uuid: str):
		return await FileDAL.get_or_none(self.user.id, uuid)

	@router.patch("/rename/{uuid}/{new_name}")
	async def rename(self, uuid: str, new_name: str):
		updated_count = await FileDAL.update(self.user.id, uuid=uuid, name=new_name)
		if not updated_count:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'file {uuid} does not exist'
			)

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

		folder = await FolderDAL.get_db_model_or_none(owner=self.user.id, uuid=folder_uuid)
		if not folder:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'folder {folder_uuid} does not exist'
			)

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

	@router.get("/download/{uuid}")
	async def download_file(self, uuid: str):
		file = await FileDAL.get_db_model_or_none(owner=self.user.id, uuid=uuid)
		if not file:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=f'file {uuid} does not exist'
			)

		message = await self.bot.get_messages(self.chat, ids=file.tg_message_id)
		return StreamingResponse(
			fast_telethon.iter_download(self.bot, message.document)
		)
