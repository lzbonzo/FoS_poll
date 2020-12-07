from rest_framework import serializers

from fos_poll.models import Question, Poll, Answer


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_right']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'text', 'answer_type', 'answers']
        depth = 1

    def get_fields(self):
        fields = super().get_fields()
        fields['answers'] = AnswerSerializer(many=True)
        return fields


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ['id', 'title', 'date_of_begin', 'date_of_end', 'description', 'questions']
        depth = 1

    def get_fields(self):
        fields = super().get_fields()
        fields['questions'] = QuestionSerializer(many=True)
        return fields

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)
        for question_data in questions:
            print(question_data)
            answers = question_data.pop('answers')
            question = Question.objects.create(poll=poll, **question_data)
            for answer_data in answers:
                Answer.objects.create(question=question, **answer_data)
        return poll

    def update(self, instance, validated_data):
        print(validated_data)
        questions = validated_data.pop('questions')
        poll = Poll.objects.filter(id=validated_data['id']).update(**validated_data)
        for question_data in questions:
            print(question_data)
            answers = question_data.pop('answers')
            Question.objects.filter(id=question_data['id']).update(**question_data)
            for answer_data in answers:
                Answer.objects.filter(id=answer_data['id']).update(**answer_data)
        return poll


