from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=50)
    date_of_begin = models.DateField(auto_now_add=False)
    date_of_end = models.DateField()
    description = models.TextField(max_length=200, blank=True)


class Question(models.Model):
    CHOICES = [('o', 'Выбрать один'),  ('f', 'Выбрать несколько'),
                                            ('t', 'Текст')]
    text = models.TextField(max_length=200)
    answer_type = models.CharField(max_length=50, choices=CHOICES, default='Выбрать один')
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, default=None)


class Answer(models.Model):

    answer = models.CharField(max_length=50)
    is_right = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None)
