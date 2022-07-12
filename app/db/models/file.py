from tortoise import fields

from app.db.models.abstract_resource import AbstractResource


class File(AbstractResource):
    owner = fields.ForeignKeyField('models.User', related_name='files')
    folder = fields.ForeignKeyField('models.Folder', related_name='files')
    tg_message_id = fields.BigIntField()

    class Meta:
        table: str = 'files'

    class PydanticMeta:    
        include = ['name', 'is_public', 'created_at', 'modified_at', 'uuid']
        optional = ['created_at', 'modified_at', 'uuid']
