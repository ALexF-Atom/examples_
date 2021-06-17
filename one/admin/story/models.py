from django.db import models
from django.contrib.postgres.fields import ArrayField
from levels.models import ModelLevel
from script.models import ModelScript
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class ModelStories(models.Model):
    ...
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    priority = models.SmallIntegerField(default=10)
    duration = models.SmallIntegerField(default=15)
    preview_image = RichTextUploadingField(verbose_name='Изображение для превью',
                                           db_column='preview',
                                           config_name='image',
                                           blank=True, null=True)
    text_preview = RichTextField(verbose_name='Текст для превью',
                                 config_name='text',
                                 blank=True, null=True)
    preview_background = models.ForeignKey(verbose_name="Фон превью",
                                           to='service.Background',
                                           on_delete=models.SET_NULL,
                                           related_name='story_preview_background',
                                           blank=True, null=True)
    ...
  

    class Meta:
        db_table = 'model_stories'

    def __str__(self):
        return self.name or self.preview


class ModelStoryContent(models.Model):
    ...
    story = models.ForeignKey(
        ModelStories, models.CASCADE, blank=True, null=True)
    order = models.SmallIntegerField(blank=True, null=True)
    type_content = models.CharField(max_length=32, choices=TYPE_CONTENT)
    name = models.CharField(max_length=128)
    content = RichTextUploadingField(verbose_name='Главный контент',
                                     blank=True, null=True,
                                     config_name='image')
    content_background = models.ForeignKey(verbose_name="Цвет фона",
                                           to='service.Background',
                                           on_delete=models.SET_NULL,
                                           blank=True, null=True,
                                           related_name='story_content_bckground')
    content_text = RichTextField(
        verbose_name='Текст для стори', blank=True, null=True, config_name='text')
    ...
   

    class Meta:
        db_table = 'model_story_content'
        ordering = ['story', 'order']
        

    def __str__(self):
        return self.name or self.story
