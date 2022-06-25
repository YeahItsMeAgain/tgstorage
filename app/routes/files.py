from fastapi import APIRouter, Depends
from telethon import TelegramClient
from starlette.requests import Request
from fastapi_restful.cbv import cbv

from app import fast_telethon
from app.db.schemas.user import SessionUser
from app.dependencies.auth import get_current_user
from app.dependencies.connect_bot import connect_bot

router = APIRouter(
	prefix='/files',
	tags=['files'],
	responses={404: {"description": "Not found"}}
)


@cbv(router)
class Files:
	bot: TelegramClient = Depends(connect_bot)
	user: SessionUser = Depends(get_current_user)

	@router.post("/upload")
	async def create_file(self, request: Request):
		def progress_callback(current, total):
			print(f'{current * 100 / total}%')

		await self.bot.send_file(
			self.user.chat_id,
			await fast_telethon.upload_from_request(self.bot, request, progress_callback)
		)
		return {'status': 'done'}
