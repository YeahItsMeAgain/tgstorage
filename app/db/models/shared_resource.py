from enum import Enum
from tortoise import fields, models

class SharedResourcePermission(str, Enum):
    view = 'view'
    edit = 'edit'

class SharedResource(models.Model):
    id = fields.IntField(pk=True)
    file = fields.ForeignKeyField('models.File', related_name='shares', null=True)
    folder = fields.ForeignKeyField('models.Folder', related_name='shares', null=True)
    user = fields.ForeignKeyField('models.User', related_name='shares')
    permission = fields.CharEnumField(SharedResourcePermission, default=SharedResourcePermission.view)

    class Meta:
        table: str = 'shared_resources'
