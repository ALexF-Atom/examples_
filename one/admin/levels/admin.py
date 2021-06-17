
import levels
from django import forms
from django.contrib import admin
from django.contrib.postgres import fields
from django.contrib.postgres.fields.array import ArrayField
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.forms import widgets
from django.utils.safestring import mark_safe
from .models import ModelEvent, ModelLevel
from event_management.models import ModelEventKey


@admin.register(ModelEvent)
class AdminModelEvent(admin.ModelAdmin):

    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(
            attrs={'size': '18'})},
        models.TextField: {'widget': forms.Textarea(
            attrs={'rows': 2, 'cols': 100})},
    }

    list_display = [...]
    list_filter = ['event_level']
    list_editable = ['event_level', ]
    # raw_id_fields = ['event_event_key']
    ordering = ('event_level', 'event_stage')
    readonly_fields = ('preview_background',)

    fieldsets = (
        ('Главные настройки', {
            'classes': ('wide',),
            'fields':  (...)
        }),
        ('Общие настройки', {
            'classes': ('wide',),
            'fields':  (...)
        }),
        ('Дополнительные настройки', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
    )

    def preview_background(self, obj):
        return obj.event_background.color_view()


class EventInline(admin.StackedInline):
    model = ModelEvent
    extra = 0
    classes = ['wide']
    readonly_fields = ('preview_background',)

    formfield_overrides = {
        models.IntegerField: {'widget': forms.TextInput(
            attrs={'size': '40', 'placeholder': "Введите числовое значение"})},
        models.CharField: {'widget': forms.TextInput(
            attrs={'size': '40'})},
        models.TextField: {'widget': forms.Textarea(
            attrs={'rows': 2, 'cols': 60})},
        models.ForeignKey: {'widget': forms.Select(
            attrs={'style': 'width: 300px;'})}
    }

    fieldsets = (
        ('Главные настройки', {
            'classes': ('wide', 'collapse'),
            'fields':  (...)
        }),
    )

    def preview_background(self, obj):
        return obj.event_background.color_view()


@admin.register(ModelLevel)
class AdminLevel(admin.ModelAdmin):
    list_display = (...)

    readonly_fields = ('preview_background',)
    list_editable = ('level_enabled',)
    inlines = [EventInline]

    formfield_overrides = {
        models.IntegerField: {'widget': forms.TextInput(
            attrs={'size': '60', 'placeholder': "Введите числовое значение"})},
        models.CharField: {'widget': forms.TextInput(
            attrs={'size': '60'})},
        models.TextField: {'widget': forms.Textarea(
            attrs={'rows': 2, 'cols': 60})},
        ArrayField: {'widget': forms.Textarea(
            attrs={'rows': 2, 'cols': 60})},
        models.ForeignKey: {'widget': forms.Select(
            attrs={'style': 'width: 300px;'})}
    }

    fieldsets = (
        ('Общие настройки', {
            'classes': ('wide',),
            'fields':  (...)
        }),
        ('Настройки', {
            'classes': ('wide',),
            'fields':  (...)
        }),
        ('Дополнительные настройки', {
            'classes': ('wide', 'collapse',),
            'fields':  (...)
        }),
    )

    def preview_background(self, obj):
        return obj.level_background.color_view()
