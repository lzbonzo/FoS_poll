from django import forms
from django.forms import modelformset_factory

from fos_poll.models import Poll, Question


class PollForm(forms.ModelForm):

    title = forms.CharField(label='Название:', max_length=50)
    date_of_begin = forms.DateField(label='Дата старта: ')
    date_of_end = forms.DateField(label='Дата окончания:')
    description = forms.CharField(widget=forms.Textarea, label='Описание:')

    class Meta:
        model = Poll
        fields = '__all__'


class QuestionForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea, initial='Введите текст вопроса')
    answer_type = forms.Select(choices=Question.CHOICES)

    class Meta:
        model = Question
        fields = ['text', 'answer_type']


QuestionFormSet = modelformset_factory(Question, fields=('text', 'answer_type'), extra=0)