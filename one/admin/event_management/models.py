
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms
from django.db import models
from django.utils import tree


class Achievement(models.Model):
    POSITION = (
        ('bottom', 'bottom'),
        ('center', 'center'),
        ('top', 'top')
    )

    tag = models.ForeignKey(
        'service.ModelTag', on_delete=models.SET_NULL, null=True)
    achievement_name = models.CharField(max_length=32)

    achievement_title = models.CharField(max_length=128,
                                         blank=True, null=True)
    achievement_text = models.TextField(blank=True, null=True)

    achievement_image = RichTextUploadingField(verbose_name='Картинка',
                                               config_name='image',
                                               default='<img alt="" src="https://practiqa-media.s3.amazonaws.com/media/media/2021/06/02/tick.png" style="height:226px; width:226px" />',
                                               blank=True, null=True)
    position_image = models.CharField(max_length=32,  choices=POSITION,
                                      default='center',
                                      null=True, blank=True)

    achievement_background = models.ForeignKey(
        'service.Background', models.SET_NULL, blank=True, null=True)
    achievement_button = models.ForeignKey(
        'service.Button', models.PROTECT, blank=True, null=True)
    position_button = models.CharField(max_length=32, choices=POSITION,
                                       default='bottom',
                                       blank=True, null=True)
    share_image = RichTextUploadingField(verbose_name='Картинка для шаринга',
                                         config_name='image',
                                         blank=True, null=True)
    description_rule = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'achievement'

    def __str__(self):
        return f"{self.achievement_name} ID[{self.id}]"

    def get_event_key(self):
        return e.slug if (e := self.event_key.first()) else "Warning! FREE!"


class UserAction(models.Model):
    ACTION_KEY_CUSTOM = (...)

    DAY_WEEK = (...)
    ...
    class Meta:
        db_table = 'user_action'


class ActionUserSettings(models.Model):
    event_key = models.ForeignKey(
        'ModelEventKey', models.CASCADE, blank=True, null=True)
    action = models.ForeignKey(
        UserAction, models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'action_user_settings'


class ModelEventKey(models.Model):
    ...
    class Meta:
        db_table = 'model_event_key'

    def __str__(self):
        return f'{self.slug}'


    def event_info(self):
        if self.event:
            return f"ID={self.event.id} and Stage={self.event.event_stage}"
        return "Empty"



class RulesEvent(models.Model):
    event_key = models.ForeignKey(ModelEventKey,
                                           on_delete=models.CASCADE)
    event = models.ForeignKey(
        'levels.ModelEvent', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'rules_event'


class RulesLevel(models.Model):   
    event_key = models.ForeignKey(ModelEventKey,
                                           on_delete=models.CASCADE)
    level = models.ForeignKey(
        'levels.ModelLevel', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'rules_level'


class RulesStory(models.Model):
    ACT = (...)
    
    TYPE = (...)

    ...

    class Meta:
        db_table = 'rules_story'



class RulesScript(models.Model):
    ACT = (...)
    TYPE = (...)
    ...
    class Meta:
        db_table = 'rules_script'



class RulesHelper(models.Model):
    event_key = models.ForeignKey(ModelEventKey,
                                           on_delete=models.CASCADE)
    ...
    class Meta:
        db_table = 'rules_helper'


class RulesButton(models.Model):
    event_key = models.ForeignKey(ModelEventKey,
                                           on_delete=models.CASCADE)
    ...

    class Meta:
        db_table = 'rules_button'





class ModelAction(models.Model):
    ...

    class Meta:
        db_table = 'model_action'
