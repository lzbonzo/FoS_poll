from collections import OrderedDict

from fos_poll.serializers import PollSerializer


def poll_data_serialize(post_data):
    """ Prepare request.POST data to save"""
    questions = OrderedDict()
    is_right_list = []
    for field, value in post_data.items():
        if 'question' in field:
            field_splitted = field.split('_')
            question = '_'.join(field_splitted[:2])
            if len(field_splitted) != 2:
                field_name = '_'.join(field_splitted[2:])
                if not questions.get(question):
                    questions[question] = {}
                    if not questions[question].get('answers'):
                        questions[question]['answers'] = []
                if field_name == 'right_answer':
                    answer = OrderedDict()
                    answer['text'] = value
                    answer['is_right'] = True
                    questions[question]['answers'].append(answer)
                elif field_name == 'isRight':
                    is_right_list.extend(post_data.getlist(field))
                else:
                    if 'answerOption' in field_name:
                        answer = OrderedDict()
                        answer['text'] = value
                        answer['is_right'] = False
                        questions[question]['answers'].append(answer)
                    else:
                        questions[question][field_name] = value

    # Check answers in checkboxes
    if is_right_list:
        for option in is_right_list:
            splitted_option_name = option.split('_')
            question = '_'.join(splitted_option_name[:2])
            number_of_right_answer = int(splitted_option_name[-1]) - 1
            questions[question]['answers'][number_of_right_answer]['is_right'] = True
    return questions


def check_user_answers(answers_to_check, context):
    """Check user answers. right or not"""
    right_answers_amount = 0
    poll_answers = PollSerializer(context['poll']).data['questions']

    for right_answers, user_answers in zip(poll_answers, answers_to_check.values()):
        user_answers['answer_type'] = right_answers['answer_type']
        user_answers['text'] = right_answers['text']
        for answer in right_answers['answers']:
            del answer['id']
        right_answer = right_answers['answers'][0]

        if right_answers['answers'] == user_answers['answers'] \
                or (right_answers['answer_type'] == 't' and
                    right_answer['text'].lower() == user_answers['answers'][0]['text'].lower()):
            right_answers_amount += 1
        for right_answer, user_answer in zip(right_answers['answers'], user_answers['answers']):
            if right_answer == user_answer or \
                    (user_answers['answer_type'] == 't' and
                     right_answer['text'].lower() == user_answers['answers'][0]['text'].lower()):
                user_answer['user_is_right'] = True
            else:
                user_answer['user_is_right'] = False
            if user_answers['answer_type'] == 't':
                user_answer['right_answer'] = right_answer['text']
                user_answer['user_answer'] = user_answer['text']

    return right_answers_amount, answers_to_check