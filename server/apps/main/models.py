from django.conf import settings
from django.db import models
from typing_extensions import final


@final
class StarWarsCollection(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modifiet_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name = 'StarWarsCollection'
        verbose_name_plural = 'StarWarsCollections'

    def __str__(self) -> str:
        return self.filename

    @property
    def filename(self):
        return f'{self.id}.csv'

    @property
    def filepath(self):
        return str(settings.RUNTIME_DIR / self.filename)
