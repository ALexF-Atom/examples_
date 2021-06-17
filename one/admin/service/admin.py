from django.contrib import admin
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

from .models import (GroupHobby,
                     Button, Background, TimeInterval, ModelTag,
                     Icon, IconState,
                     Day, GroupDay, NameGroupDay)
from hobby.models import ModelHobby
# Register your models here.


@admin.register(Button)
class AdminButton(admin.ModelAdmin):
    model = Button
    list_display = ['name', "background_view"]

    def background_view(self, obj):
        if obj.button_background is None:
            return ""
        colors = obj.button_background.colors
        vector = obj.button_background.vector
        if len(colors) == 1:
            return mark_safe(
                f'<div style="background-color:{colors[0]}; width:120px;">{obj.button_text}</div>')
        elif len(colors) > 1:
            return mark_safe(
                f'<div style="background-image: linear-gradient({vector}deg ,{",".join(colors)}); width:120px;">{obj.button_text}</div>'
            )


@admin.register(Background)
class AdminBackground(admin.ModelAdmin):
    model = Background
    list_display = ['name', 'color_view']

    class Media:
        js = (
            'js/colors-view.js',
        )


@admin.register(TimeInterval)
class AdminInterval(admin.ModelAdmin):
    model = TimeInterval


@admin.register(ModelTag)
class AdminModelTag(admin.ModelAdmin):
    model = ModelTag


class InlineIconState(admin.TabularInline):
    model = IconState
    extra = 0


@admin.register(Icon)
class AdminIcon(admin.ModelAdmin):
    list_display = ['title_icon']
    inlines = [InlineIconState]


