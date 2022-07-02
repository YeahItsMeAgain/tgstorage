from tortoise import fields

from app.db.models.abstract_resource import AbstractResource
from .file import File


class Folder(AbstractResource):
    owner = fields.ForeignKeyField('models.User', related_name='folders')
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
        exclude = [
            'owner', 'sub_folders.parent',
            'files.owner', 'files.folder'
        ]
        max_recursion = 2
