from enum import Enum
from tortoise import fields
from tortoise.models import Model

# The name of the methods used to edit the editors of the resources.
class EditorMethod(str, Enum):
    Add = 'add'
    Remove = 'remove'

class SharedResource(Model):
    id = fields.IntField(pk=True)
    file = fields.ForeignKeyField('models.File', related_name='shares', null=True)
    folder = fields.ForeignKeyField('models.Folder', related_name='shares', null=True)
    shared_user_email = fields.CharField(max_length=320)
    class Meta:
        table: str = 'shared_resources'
