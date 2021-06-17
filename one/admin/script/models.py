from django.db import models
from django.utils.html import format_html
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.aggregates import ArrayAgg
from jsonfield import JSONField


AnswerType = [...]


class ScriptTags(models.Model):
    tag = models.ForeignKey(
        'service.ModelTag', models.CASCADE, blank=True, null=True)
    script = models.ForeignKey(
        'ModelScript', models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'script_tags'



class ModelScript(models.Model):
    tags = models.ManyToManyField('service.ModelTag',
                                  through=ScriptTags,
                                  through_fields=('script','tag'))
    name = models.TextField(verbose_name='Название скрипта',
                            unique=True)
  
    class Meta:
        db_table = 'model_script'
        verbose_name = 'Анкета'
        verbose_name_plural = 'Список анкет'

    def __str__(self):
        return f'{self.id}: {self.name}'



class ModelAnswer(models.Model):
    answer = models.CharField(verbose_name='Ответ:',
                              max_length=128, unique=True)

    class Meta:
        db_table = 'model_answer'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Список ответов'

    def __str__(self):
        return format_html(self.answer)


class ModelQuest(models.Model):
    quest = models.TextField(verbose_name='Вопрос:', unique=True)

    class Meta:
        db_table = 'model_quest'
        verbose_name = 'Вопросы'
        verbose_name_plural = 'Список вопросов'

    def __str__(self):
        return format_html(f'{self.quest}')

    def _answer(self):
        return self.quest_answer.values_list('answer_id')


class QuestTags(models.Model):
    tag = models.ForeignKey(
        'service.ModelTag', models.CASCADE, blank=True, null=True)
    quest = models.ForeignKey(
        ModelQuest, models.CASCADE, blank=True, null=True)

    class Meta: 
        db_table = 'quest_tags'


class ModelScriptQuest(models.Model):

    ...
    
    class Meta:
        db_table = 'model_script_quest'
        verbose_name = 'Добавить в анкету'
        verbose_name_plural = 'Конструктор анкет'

    def __str__(self):
        return '; '.join(self.quest.quest_answer.values_list('answer__answer', flat=True))


class ModelQuestAnswer(models.Model):
    ...

    class Meta:
        db_table = 'model_quest_answer'
        verbose_name = 'Вопрос-Ответ'
        verbose_name_plural = 'Вопрос-ответы'
        ordering = ['order']
        constraints = (models.UniqueConstraint(fields=['quest_id', 'answer_id', 'order'],
                                               name='unq_quest_answer'),)

    def __str__(self):
        return ""


class AnswerTags(models.Model):
    ...
    class Meta:
        
        db_table = 'answer_tags'
