from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class ModelFsm(models.Model):
    ...

    class Meta:
        
        db_table = 'model_fsm'


class ModelFsmHobby(models.Model):
    ...

    class Meta:
        
        db_table = 'model_fsm__hobby'
        unique_together = (('user_id', 'user_hobby_id'),)
