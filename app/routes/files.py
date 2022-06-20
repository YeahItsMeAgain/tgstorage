import hashlib

from fastapi import APIRouter, Depends
from telethon.tl import types
from telethon import TelegramClient, helpers
from starlette.requests import Request
from fastapi_restful.cbv import cbv

from app.utils import chunker
from app.dependencies.connect_bot import connect_bot
from app.fast_telethon import ParallelTransferrer
from app import bot

# TODO: use a robust logger, maybe loguru

router = APIRouter(
    prefix='/files',
    tags=['files'],
    responses={404: {"description": "Not found"}}
)

@cbv(router)
class Files:
	bot: TelegramClient = Depends(connect_bot)

	@router.post("/upload")
	async def create_file(self, request: Request):
		file_id = helpers.generate_random_long()
		file_size = int(request.headers['content-length'])
		hash_md5 = hashlib.md5()
		uploader = ParallelTransferrer(self.bot)
		part_size, part_count, is_large = await uploader.init_upload(file_id, file_size)
		print(f'{file_size=} {part_count=}, {is_large=}')

		i = 0
		# making this run in asyncio.wait will be better but seems like this needs to run one after another
		async for big_chunk in request.stream():
			for chunk in chunker(big_chunk, part_size):
				i += 1
				print(f'chunk {i=}, {len(chunk)=}')
				if not is_large:
					hash_md5.update(chunk)

				await uploader.upload(chunk)
		await uploader.finish_upload()

		file = types.InputFileBig(file_id, part_count, "upload") if is_large\
			else types.InputFile(file_id, part_count,
								"upload", hash_md5.hexdigest())

		await bot.send_file("YeahItsMeAgain", file)
		return {'status': 'done'}