from django.db import models
from django.forms import ModelChoiceField, Form, ChoiceField, Select


# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=50)
    date_of_begin = models.DateField(auto_now_add=False)
    date_of_end = models.DateField()
    description = models.TextField(max_length=100)
    # question = models.ForeignKey('Question', on_delete=models.CASCADE)


class Question(models.Model):
    text = models.TextField(max_length=50)
    answer_type = models.CharField(max_length=50,
                                   choices=[('o', 'choose one'),  ('f', 'choose few'), ('t', 'text')], default='text')
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, default=None)


