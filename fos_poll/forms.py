from django import forms
from django.forms import inlineformset_factory


from fos_poll.models import Poll, Question, Answer


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text', 'is_right']


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, initial='Введите текст вопроса')
    answer_type = forms.Select(choices=Question.CHOICES)

    class Meta:
        model = Question
        fields = ['text', 'answer_type']


QuestionFormSet = inlineformset_factory(Poll, Question, exclude=('poll',), extra=0)


class PollForm(forms.ModelForm):
    DATE_INPUT_FORMATS = ['%d.%m.%Y']

    title = forms.CharField(label='Название:', max_length=50)
    date_of_begin = forms.DateField(label='Дата старта: ', input_formats=DATE_INPUT_FORMATS)
    date_of_end = forms.DateField(label='Дата окончания:', input_formats=DATE_INPUT_FORMATS)
    description = forms.CharField(widget=forms.Textarea, label='Описание:', required=False)


    class Meta:
        model = Poll
        fields = ('title', 'date_of_begin', 'date_of_end', 'description')


AnswerFormSet = inlineformset_factory(Question, Answer, exclude=('poll',), extra=0)
