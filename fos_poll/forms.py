from django import forms
from django.forms import inlineformset_factory

from fos_poll.models import Poll, Question, Answer


AnswerFormSet = inlineformset_factory(Question, Answer, exclude=('poll',), extra=0)


class AnswerForm(forms.ModelForm):
    text = forms.CharField(label='Ответ:', required=True)
    is_right = forms.BooleanField(required=False)

    class Meta:
        model = Answer
        exclude = ('question', )


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'required': 'true'}), initial='Введите текст вопроса', required=True)
    answer_type = forms.Select(choices=Question.CHOICES)

    class Meta:
        model = Question
        fields = ['text', 'answer_type']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_formset = AnswerFormSet(instance=self.instance,
                                            data=self.data or None,
                                            prefix=self.prefix)

    def is_valid(self):
        return (super().is_valid() and
                all([AnswerForm(answer).is_valid() for answer in self.data['answers']]))

    def save(self, commit=True):
        assert commit is True
        res = super().save(commit=commit)
        for answer in self.data['answers']:
            AnswerForm(instance=Answer(question=self.instance), data=answer).save()
        return res


class PollForm(forms.ModelForm):
    DATE_FORMAT = "%d.%m.%Y"

    title = forms.CharField(label='Название:')
    date_of_begin = forms.DateField(input_formats=("%d.%m.%Y", ),
                                    widget=forms.widgets.DateInput(format=DATE_FORMAT), label='Дата начала:')
    date_of_end = forms.DateField(input_formats=("%d.%m.%Y", ),
                                  widget=forms.widgets.DateInput(format=DATE_FORMAT), label='Дата окончания:')
    description = forms.Textarea()

    class Meta:
        model = Poll
        fields = '__all__'


QuestionFormSet = inlineformset_factory(Poll, Question, form=QuestionForm, exclude=('poll',), extra=0)
