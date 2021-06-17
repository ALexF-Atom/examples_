from django.contrib import admin
from django import forms
from django.contrib.postgres import fields
from django.db import models
from django.contrib.postgres.fields.array import ArrayField
from django.db.models import query
from django.db.models.expressions import Exists, OuterRef

from . import models as em
from levels.models import ModelEvent, ModelLevel
from helper.models import ModelHelper
from service.models import Button
from script.models import ModelScript
from story.models import ModelStories, ModelStoryContent
from users.models import ModelUserEvent, ModelUserRelationAction


class InlineRulesLevel(admin.TabularInline):
    model = em.RulesLevel
    extra = 0


class InlineRulesEvent(admin.TabularInline):
    model = em.RulesEvent
    extra = 0


class InlineRulesStory(admin.TabularInline):
    model = em.RulesStory
    extra = 0


class InlineRulesScript(admin.TabularInline):
    model = em.RulesScript
    extra = 0


class InlineRulesHelper(admin.TabularInline):
    model = em.RulesHelper
    extra = 0


class InlineRulesButton(admin.TabularInline):
    model = em.RulesButton
    extra = 0


class InlineRulesActionUser(admin.TabularInline):
    model = em.UserAction
    extra = 0


class InlineRulesActionSettings(admin.StackedInline):
    model = em.ActionUserSettings
    extra = 0


@admin.register(ModelUserEvent)
class UserEventStage(admin.ModelAdmin):
    list_display = ['user_uid', 'user_data',
                    'event_completed', 'event', 'event_info']
    list_filter = ['event']
    list_select_related = ('user', 'event')
    ordering = ('event_completed',)
    list_max_show_all = 25


@admin.register(ModelUserRelationAction)
class LoggingUserAction(admin.ModelAdmin):
    list_display = ['user', 'action_key', 'related_name', 'key']
    list_max_show_all = 25
    ordering = ('created_at',)
    list_filter = ('user', 'action_key',)


class AchievmentFree(admin.SimpleListFilter):
    title = 'NotEventKey'
    parameter_name = 'is_key'

    def lookups(self, request, model_admin):
        return (
            ('free', 'FREE'),
            ('busy', 'BUSY'),

        )

    def queryset(self, request, queryset):
        if self.value() == 'free':
            return queryset.filter(event_key__isnull=True)
            # return queryset.filter(~Exists(ModelEventKey.objects.filter(achievement__id=OuterRef('id'))))
        if self.value() == 'busy':
            # return queryset.filter(Exists(ModelEventKey.objects.filter(achievement__id=OuterRef('id'))))
            return queryset.filter(event_key__isnull=False)


class FormAchievement(forms.ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'achievement_background': forms.Select(attrs={
                'class': 'data-choise'
            })
        }


@admin.register(em.Achievement)
class AdminAchievments(admin.ModelAdmin):
    list_display = ('achievement_name', 'tag', 'get_event_key',)
    readonly_fields = ('preview',)
    list_filter = ('tag', AchievmentFree, 'event_key__level')
    ordering = ('tag',)
    form = FormAchievement
    list_select_related = True

    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(
            attrs={'size': '80'})},
        models.TextField: {'widget': forms.Textarea(
            attrs={'rows': 2, 'cols': 100})},
        ArrayField: {'widget': forms.Textarea(
            attrs={'rows': 2, 'cols': 100})},
    }

    fieldsets = (
        ('Настройки', {
            'classes': ('wide',),
            'fields': (...)
        }),
        ('Дополнительный Настройки', {
            'classes': ('wide', 'collapse'),
            'fields': ('share_image',)
        }),
    )

    def preview(self, obj):
        if obj.achievement_background:
            return obj.achievement_background.color_view()
        return ""

    class Media:
        js = (
            'js/preview.js',
        )


# добавить форму выбора level, event, buttons, helper, story,
@admin.register(em.ModelEventKey)
class AdminEventKey(admin.ModelAdmin):
    list_display = ['id', '__str__', 'tag',
                    'achievement', 'event_info', ]
    list_filter = ['tag', 'event__event_level']
    ordering = ('level', 'event__event_stage',)
    list_display_links = ('__str__', )
    raw_id_fields = ('achievement', 'event')
    list_editable = ('tag',)
    list_select_related = ('achievement', 'level', 'event')
    
    inlines = [InlineRulesButton, InlineRulesHelper,
               InlineRulesStory, InlineRulesScript,
               InlineRulesEvent, InlineRulesLevel,
               InlineRulesActionSettings]
    
    formfield_overrides = {
        models.IntegerField: {'widget': forms.TextInput(
            attrs={'size': '30'})},
        models.CharField: {'widget': forms.TextInput(
            attrs={'size': '80'})},
        models.TextField: {'widget': forms.Textarea(
            attrs={'rows': 2, 'cols': 100})},
        ArrayField: {'widget': forms.Textarea(
            attrs={'rows': 2, 'cols': 100})},
    }


@admin.register(em.ActionUserSettings)
class AdminActionSettings(admin.ModelAdmin):
    ...


@admin.register(em.UserAction)
class AdminUserAction(admin.ModelAdmin):
    inlines = [InlineRulesActionSettings]
