from django.contrib.postgres import fields
from django.forms.widgets import Textarea
from django.forms.fields import CharField
from django import forms
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.forms import SimpleArrayField

from . import models as m


class Base_(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
        ArrayField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }


class InlineScriptQuest(admin.TabularInline):
    model = m.ModelScriptQuest
    extra = 0


class InlineQuestAnswer(admin.TabularInline):
    model = m.ModelQuestAnswer
    extra = 0


class FormScript(forms.ModelForm):
    class Meta:
        model = m.ModelScript
        fields = '__all__'


class InlineScriptTags(admin.TabularInline):
    model = m.ModelScript.tags.through

    # model = m.ScriptTags
    extra = 0


class FormQuestAnswer(forms.ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'answer_background': forms.Select(attrs={
                'class': 'data-choise'})}


@admin.register(m.ModelQuestAnswer)
class AdminQuestAnswer(admin.ModelAdmin):
    list_display = (...)
    readonly_fields = ('preview',)
    form = FormQuestAnswer

    list_filter = (...)

    def preview(self, obj):
        if obj.answer_background:
            return obj.answer_background.color_view()
        return ""

    class Media:
        js = (
            'js/preview.js',
        )


@admin.register(m.ModelScript)
class AdminScript(Base_):
    list_display = ['__str__', '_tags']
    form = FormScript
    inlines = [InlineScriptTags, InlineScriptQuest]

    def _tags(self, obj):
        data = obj.tags.all().values_list('tag', flat=True)
        return ", ".join(data)


@admin.register(m.ModelQuest)
class AdminQuest(Base_):
    inlines = [InlineQuestAnswer]


@admin.register(m.ModelAnswer)
class AdminAnswer(Base_):
    model = m.ModelAnswer

admin.site.register(m.ScriptTags)
