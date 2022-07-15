from tortoise import fields

from app.db.models.abstract_resource import AbstractResource


class File(AbstractResource):
    owner = fields.ForeignKeyField('models.User', related_name='owned_files')
    creator = fields.ForeignKeyField('models.User', related_name='created_files')
    editors = fields.ManyToManyField("models.User", related_name="files", through="file_user")
    folder = fields.ForeignKeyField('models.Folder', related_name='files')
    tg_message_id = fields.BigIntField()

    class Meta:
        table: str = 'files'

    class PydanticMeta:
        exclude_raw_fields = False
        include = ['owner', 'creator', 'name', 'is_public', 'created_at', 'modified_at', 'uuid', 'editors']
        optional = ['created_at', 'modified_at', 'uuid']
