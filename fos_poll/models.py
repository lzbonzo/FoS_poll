from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название:')
    date_of_begin = models.DateField(auto_now_add=False, verbose_name='Дата начала:')
    date_of_end = models.DateField(verbose_name='Дата окончания:')
    description = models.TextField(max_length=200, blank=True, verbose_name='Описание:')


class Question(models.Model):
    CHOICES = [('o', 'Выбрать один'),  ('f', 'Выбрать несколько'),
                                            ('t', 'Текст')]
    text = models.TextField(max_length=200)
    answer_type = models.CharField(max_length=50, choices=CHOICES, default='Выбрать один')
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, default=None, related_name='questions')


class Answer(models.Model):

    text = models.CharField(max_length=50)
    is_right = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None, related_name='answers')
