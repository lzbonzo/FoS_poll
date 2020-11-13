from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db import models
from django.forms import ChoiceField, Form, Select

# Register your models here.
from django.utils.html import format_html

from fos_poll.models import Poll, Question


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    can_delete = True
    # TODO сделать кнопку удаления вопроса прямо из опроса
    #  - Авторизация в системе
    #  - Подумать над интерфейсом для админа (нужна авторизация, возможно оставить джанговскую авторизацию




    def delete_button(self, obj):
        return format_html('<a class="btn" href="/admin/fos_poll/my_model/{}/delete/">Delete</a>', obj.id)


class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_of_begin', 'date_of_end']
    inlines = [QuestionInline]

    def get_readonly_fields(self, request, obj=None):
        """ После создания поле "дата старта/date_of_begin" у опроса менять нельзя """
        if obj:  # editing an existing object
            return self.readonly_fields + ('date_of_begin',)
        return self.readonly_fields






admin.site.register(Poll, PollAdmin)
admin.site.register(Question)

