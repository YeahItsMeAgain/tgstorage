from tortoise import fields
from tortoise.models import Model

class SharedResource(Model):
    id = fields.IntField(pk=True)
    file = fields.ForeignKeyField('models.File', related_name='shares', null=True)
    folder = fields.ForeignKeyField('models.Folder', related_name='shares', null=True)
    owner = fields.ForeignKeyField('models.User', related_name='shares')
    shared_user_email = fields.CharField(max_length=320)
    class Meta:
        table: str = 'shared_resources'
