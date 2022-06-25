from uuid import uuid4
from tortoise import fields, models

from app.db.models.timestamp_mixin import TimestampMixin

class AbstractResource(TimestampMixin, models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    link_uuid = fields.UUIDField(unique=True, default=uuid4)

    class Meta:
        abstract = True
