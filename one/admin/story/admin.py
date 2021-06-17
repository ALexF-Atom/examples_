from django.contrib import admin
 
from django import forms
from django.contrib.postgres import fields
from django.db import models
from django.forms import TextInput, Textarea
from django.contrib.postgres.fields import ArrayField

from .models import ModelStories, ModelStoryContent


class InlineStoryContent(admin.StackedInline):
    model = ModelStoryContent
    extra = 0
    classes = ['wide']

    fieldsets = (
        ('Общие настройки', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
                     
        }),
    )


class FormStoryContent(forms.ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'content_background': forms.Select(attrs={
                'class': 'data-choise'
            })
        }


class FormStory(forms.ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'preview_background': forms.Select(attrs={
                'class': 'data-choise'
            })
        }


@admin.register(ModelStories)
class AdminStory(admin.ModelAdmin):

    list_display = ['priority', 'name', 'active', 'date_created']
    list_display_links = ('name',)
    list_editable = ('active', 'priority')
    readonly_fields = ('preview',)
    ordering = ('-priority', '-date_created')
    inlines = [InlineStoryContent]
    form = FormStory

    fieldsets = (
        ('Настройки', {
            'classes': ('wide',),
            'fields':  (...)
        }),
        ('Настройки для главного экрана', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
        ('Дополнительные настройки стори', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
    )

    def preview(self, obj):
        if obj.preview_background:
            return obj.preview_background.color_view()
        return ""

    class Media:
        js = (
            'js/preview.js',
        )


@admin.register(ModelStoryContent)
class AdminStoryContent( admin.ModelAdmin):
    list_display = ['order', 'name', 'story', 'type_content',]
    list_editable = ('order', 'type_content')
    list_display_links = ('name',)
    readonly_fields = ('preview',)
    list_filter = ('story', 'type_content', 'story__level')
    ordering = ('story', 'order')
    form = FormStoryContent

    fieldsets = (
        ('Общие настройки', {
            'classes': ('wide',),
            'fields':  (...)
        }),
        ('Контент', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
        ('Контент без картинки', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
        ('Добавим кнопку', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
        ('Добавим вопрос', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
        ('Добавим шаринг', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
    )

    def preview(self, obj):
        if obj.content_background:
            return obj.content_background.color_view()
        return ""

    class Media:
        js = (
            'js/preview.js',
        )
