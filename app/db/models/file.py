from tortoise import fields

from app.db.models.abstract_resource import AbstractResource
from app.db.models.abstract_model import AbstractModel

class File(AbstractResource, AbstractModel):
    owner = fields.ForeignKeyField('models.User', related_name='files')
    folder = fields.ForeignKeyField('models.Folder', related_name='files')

    class Meta:
        table: str = 'files'