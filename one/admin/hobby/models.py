from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.postgres.fields import ArrayField
from jsonfield import JSONField

from helper.models import ModelHelper


class ModelHobby(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    icon = models.ForeignKey('service.Icon', models.SET_NULL, blank=True, null=True)
    is_enabled = models.BooleanField()
    
    class Meta:
        db_table = 'model_hobby'

    def __str__(self):
        return self.title


...