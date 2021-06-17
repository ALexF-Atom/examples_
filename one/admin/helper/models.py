from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models



class ModelHelper(models.Model):
    ...
        
    class Meta:
        db_table = 'model_helper'

    def __str__(self):
        return f'{self.name}: {self.text_url_for_helper}'


class HelperTags(models.Model):
    tag = models.ForeignKey(
        'service.ModelTag', models.CASCADE, blank=True, null=True)
    helper = models.ForeignKey(
        ModelHelper, models.CASCADE, blank=True, null=True)

    class Meta:
        
        db_table = 'helper_tags'
