from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class ModelLevel(models.Model):
    level_enabled = models.BooleanField(default=True)
    level_stage = models.SmallIntegerField()
    level_title = models.CharField(max_length=64)
    level_name = models.CharField(max_length=32, blank=True, null=True)
    level_image = RichTextUploadingField(verbose_name='Изображение',
                                         config_name='image',
                                         blank=True, null=True)
    level_description = models.TextField(blank=True, null=True)
    ...
    

    class Meta:
        db_table = 'model_level'

    def __str__(self):
        return f'{self.level_stage} -- {self.level_name or self.level_title}'


class ModelEvent(models.Model):
    event_level = models.ForeignKey(
        ModelLevel, models.SET_NULL, blank=True, null=True)
    event_stage = models.SmallIntegerField()
    event_title = models.CharField(max_length=64)
    event_name = models.CharField(max_length=32)
    event_image = RichTextUploadingField(verbose_name='Изображение',
                                         config_name='image',
                                         blank=True, null=True)
    event_description = models.TextField(blank=True, null=True)
    ...

    class Meta:
        db_table = 'model_event'

    def __str__(self):
        return self.event_title
