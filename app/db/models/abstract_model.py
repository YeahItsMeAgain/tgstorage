
from tortoise import models


class AbstractModel(models.Model):

    def __init__(self, *args, **kwargs):
        self.original_kwargs = kwargs.keys()
        super(AbstractModel, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    def dict(self, exclude_defaults=True):
        model_dict = {}
        for k, v in dict(self).items():
            if not isinstance(v, (int, str, bool, dict)):
                continue
            if exclude_defaults and k not in self.original_kwargs:
                continue

            model_dict[k] = v
        
        return model_dict
