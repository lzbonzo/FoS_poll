from django.contrib import admin
from django.db import models
from django.forms import ChoiceField, Form, Select

# Register your models here.
from django.utils.html import format_html

from fos_poll.models import Poll, Question


class CommonInlineConfigurationMixin(object):
    pass


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    can_delete = True
    # TODO сделать кнопку удаления вопроса прямо из опроса
    #  - Авторизация в системе
    #  - После создания поле "дата старта" у опроса менять нельзя
    #  - Подумать над интерфейсом для админа (нужна авторизация, возможно оставить джанговскую авторизацию




    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/fos_poll/my_model/{}/delete/">Delete</a>', obj.id)


class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_of_begin', 'date_of_end']
    inlines = [QuestionInline]



admin.site.register(Poll, PollAdmin)
admin.site.register(Question)

