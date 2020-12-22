from rest_framework import serializers

from fos_poll.models import Question, Poll, Answer


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_right']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answer_type', 'answers']


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'date_of_begin', 'date_of_end', 'description', 'questions']

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)
        for question_data in questions:
            answers = question_data.pop('answers')
            question = Question.objects.create(poll=poll, **question_data)
            for answer_data in answers:
                Answer.objects.create(question=question, **answer_data)
        return poll

    def update(self, instance, validated_data):
        questions = validated_data.pop('questions')
        poll = Poll.objects.filter(id=validated_data['id']).update(**validated_data)
        for question_data in questions:
            answers = question_data.pop('answers')
            Question.objects.filter(id=question_data['id']).update(**question_data)
            for answer_data in answers:
                Answer.objects.filter(id=answer_data['id']).update(**answer_data)
        return poll
