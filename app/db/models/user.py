from tortoise import fields
from tortoise.models import Model

from app.db.models.timestamp_mixin import TimestampMixin
from app.db import schemas
from .folder import Folder
from .file import File
from .shared_resource import SharedResource

class User(TimestampMixin, Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(unique=True, max_length=320, index=True)
    bot_token = fields.CharField(null=True, max_length=120)
    chat_id = fields.BigIntField(null=True)
    is_active = fields.BooleanField(default=True)

    folders: fields.ReverseRelation['Folder']
    files: fields.ReverseRelation['File']
    shared_resources: fields.ReverseRelation['SharedResource']

    async def root_folder(self):
        db_folder = await Folder.get_or_none(owner=self.id, is_root=True)
        return await schemas.Folder.from_tortoise_orm(db_folder)

    class Meta:
        table: str = 'users'

    class PydanticMeta:
        computed = ["root_folder"]
