from tortoise import fields
from tortoise.models import Model

from app.db.models.timestamp_mixin import TimestampMixin
from .folder import Folder
from .file import File
from .shared_resource import SharedResource

class User(TimestampMixin, Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=255)
    email = fields.CharField(unique=True, max_length=320, index=True)
    bot_token = fields.CharField(null=True, max_length=120)
    chat_id = fields.IntField(null=True)
    is_active = fields.BooleanField(default=True)
    root_folder = fields.ForeignKeyField('models.Folder', null=True)

    folders: fields.ReverseRelation['Folder']
    files: fields.ReverseRelation['File']
    shared_resources: fields.ReverseRelation['SharedResource']
    class Meta:
        table: str = 'users'
