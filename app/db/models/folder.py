from tortoise import fields

from app.db.models.abstract_resource import AbstractResource
from .file import File

class Folder(AbstractResource):
    owner = fields.ForeignKeyField('models.User', related_name='owned_folders')
    creator = fields.ForeignKeyField('models.User', related_name='created_folders')
    editors = fields.ManyToManyField("models.User", related_name="folders", through="folder_user")
    parent = fields.ForeignKeyField(
        'models.Folder', related_name='sub_folders', null=True
    )
    is_root = fields.BooleanField(default=False)

    files: fields.ReverseRelation['File']
    sub_folders: fields.ReverseRelation['Folder']

    class Meta:
        table: str = 'folders'

    class PydanticMeta:
        allow_cycles = True
        max_recursion = 2
        exclude = ['id']
        include = ['owner', 'creator', 'editors', 'name', 'is_public', 'created_at', 'modified_at', 'uuid']
        optional = ['created_at', 'modified_at', 'uuid']
        exclude_raw_fields = False
