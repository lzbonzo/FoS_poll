from django.contrib import admin

# Register your models here.
from fos_poll.models import Poll, Question, Answer


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    can_delete = True


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    can_delete = True


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'answer_type']
    inlines = [AnswerInline]


class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_of_begin', 'date_of_end']
    inlines = [QuestionInline]

    def get_readonly_fields(self, request, obj=None):
        """ После создания поле "дата старта/date_of_begin" у опроса менять нельзя """
        if obj:  # editing an existing object
            return self.readonly_fields + ('date_of_begin',)
        return self.readonly_fields


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
