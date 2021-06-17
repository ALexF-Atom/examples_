from django.db.models.fields import related
from hobby.models import ModelHobby
from story.models import ModelStories
from levels.models import ModelEvent, ModelLevel
from django.db import models
from jsonfield import JSONField


class ModelUser(models.Model):
    uid = models.UUIDField(primary_key=True)
    is_registered = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'model_user'

...