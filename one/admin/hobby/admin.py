from django import forms
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.contrib.postgres.fields import ArrayField
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from . import models as m


class BaseInline(admin.TabularInline):
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},  
    }


class InlineLong(BaseInline):
   ...


class InlineWhat(BaseInline):
   ...


class InlineWhere(BaseInline):
    ...



@admin.register(m.ModelHobby)
class AdminHobby(admin.ModelAdmin):
    list_display = ['title', 'description']
    
    inlines = [InlineWhat, InlineWhere, InlineLong]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }

