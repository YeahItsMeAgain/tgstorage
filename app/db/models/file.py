from tortoise import fields

from app.db.models.abstract_resource import AbstractResource

class File(AbstractResource):
    owner = fields.ForeignKeyField('models.User', related_name='files')
    folder = fields.ForeignKeyField('models.Folder', related_name='files')

    class Meta:
        table: str = 'files'