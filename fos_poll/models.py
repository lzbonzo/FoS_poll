from django.db import models


class Poll(models.Model):
    title = models.CharField('Название:', max_length=50)
    date_of_begin = models.DateField('Дата начала:', auto_now_add=False)
    date_of_end = models.DateField('Дата окончания:')
    description = models.TextField('Описание:', max_length=200, blank=True)


class Question(models.Model):
    CHOICES = [('o', 'Выбрать один'),  ('f', 'Выбрать несколько'), ('t', 'Текст')]
    text = models.TextField('Текст вопроса:', max_length=200)
    answer_type = models.CharField('Тип ответа:', max_length=50, choices=CHOICES, default='Выбрать один')
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, default=None, related_name='questions')


class Answer(models.Model):

    text = models.CharField('Текст ответа:', max_length=50)
    is_right = models.BooleanField('Верный ли ответ:')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None, related_name='answers')
