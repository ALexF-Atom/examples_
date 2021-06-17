from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.safestring import mark_safe

from hobby.models import ModelHobby
from levels.models import ModelLevel
from script.models import ModelScript
from event_management.models import ModelEventKey

class ModelTag(models.Model):
    tag = models.CharField(max_length=32)

    class Meta:
        db_table = 'model_tag'

    def __str__(self):
        return self.tag


class BackgroundTags(models.Model):
    tag = models.ForeignKey(
        ModelTag, models.DO_NOTHING, blank=True, null=True)
    background = models.ForeignKey(
        'Background', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        
        db_table = 'background_tags'



class Background(models.Model):

    name = models.CharField(max_length=32, blank=True, null=True)
    colors = models.CharField(max_length=64)
    vector = models.SmallIntegerField(blank=True, null=True, choices=VECTOR)

    class Meta:
        db_table = 'background'

    def __str__(self):
        return f'{self.name}: {self.colors}'

    def color_view(self):
        if not self.colors:
            return ""

        data = self.colors.split(',')
        if len(data) == 1:
            return mark_safe(
                '<div style="background-color:{}; height:20px; width:80px;"> </div>'.format(data[0]))
        elif len(self.colors) > 1:
            return mark_safe(
                f'<div style="background-image: linear-gradient({self.vector}deg ,{",".join(data)}); height:20px; width:80px;"> </div>'
            )


class Button(models.Model):
    tag = models.ForeignKey('service.ModelTag',
                            models.SET_NULL,
                            blank=True, null=True)
    name = models.CharField(max_length=32)
    button_text = RichTextField(verbose_name='Текст',
                                max_length=128,
                                blank=True, null=True,
                                config_name='text')
    button_id_script = models.ForeignKey(
        ModelScript, models.SET_NULL, db_column='button_id_script', null=True, blank=True)
    button_url = models.TextField(blank=True, null=True)
    button_background = models.ForeignKey(Background,
                                          models.DO_NOTHING,
                                          blank=True, null=True)
    open_in_extarnal = models.BooleanField(default=True)
   

    class Meta:
        db_table = 'button'

    def __str__(self):
        return self.name


class TimeInterval(models.Model):
    name = models.CharField(max_length=32)
    start = models.TimeField()
    end = models.TimeField()

    class Meta:
        db_table = 'time_interval'
        constraints = (models.UniqueConstraint(fields=['start', 'end'],
                                               name='unique_time'),)
        verbose_name = 'Интервал'
        verbose_name_plural = 'Временные интервалы'


class GroupNameHobby(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        
        db_table = 'group_name_hobby'


class GroupHobby(models.Model):
    group = models.ForeignKey(
        'GroupNameHobby', models.CASCADE, blank=True, null=True)
    hobby = models.ForeignKey(
        ModelHobby, models.CASCADE, null=True)

    class Meta:
        db_table = 'group_hobby'
        verbose_name = 'Группа Хобби'
        # verbose_name_plural = ''


class Day(models.Model):
    day = models.SmallIntegerField()

    class Meta:
        db_table = 'day'


class GroupDay(models.Model):
    named_group_day = models.ForeignKey(
        'NameGroupDay', models.CASCADE)
    day = models.ForeignKey(Day, models.CASCADE)

    class Meta:
        db_table = 'group_day'


class NameGroupDay(models.Model):
    title = models.CharField(max_length=32)

    class Meta:
        db_table = 'name_group_day'


class Icon(models.Model):
    title_icon = models.CharField(max_length=32)
    img_icon = RichTextUploadingField(verbose_name='Картинка',
                                      config_name='image',
                                      blank=True, null=True)

    class Meta:
        db_table = 'icon'

    def __str__(self):
        return self.title_icon


class IconState(models.Model):
    icon = models.ForeignKey(Icon, models.CASCADE)
    title_state = models.CharField(max_length=32, choices=STATE)
    color = models.ForeignKey(
        Background, models.SET_NULL, blank=True, null=True)
    opacity = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'icon_state'

    def __str__(self):
        return self.title_state

