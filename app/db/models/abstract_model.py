
from tortoise import models

class AbstractModel(models.Model):
    class Meta:
        abstract = True

    def dict(self):
        return {k: v for k, v in dict(self).items() if isinstance(v, (int, str, bool, dict))}
