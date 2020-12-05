from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# Create your views here.
from django.views.generic import TemplateView

from fos_poll.models import Poll, Question, Answer
from fos_poll.forms import PollForm, QuestionForm, AnswerFormSet


class About(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'about'
        return context


class MainPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls = Poll.objects.values('title', 'description', 'id')
        context['polls'] = polls
        return context


class PollView(TemplateView):
    template_name = 'poll.html'

    def get_context_data(self, poll_id, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = Poll.objects.filter(id=poll_id)[0]
        context['id'] = poll_id
        context['title'] = poll.title
        context['description'] = poll.description
        return context


class AdminLoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = super().get_context_data(**kwargs)
            context['message'] = '*логин или пароль введены неверно'
            return render(request, self.template_name, context)


class AdminPollsView(TemplateView):
    template_name = 'admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls = Poll.objects.values(
            'title', 'description', 'date_of_begin', 'date_of_end', 'id').order_by('-date_of_begin')
        context['polls'] = polls
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(message='Record deleted')
        poll_id = request.POST.get('id')
        Poll.objects.get(id=poll_id).delete()
        return self.render_to_response(context)


class MyPollsView(TemplateView):
    template_name = 'my_polls.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls = Poll.objects.values('title', 'description', 'id')
        context['polls'] = polls
        return context


class EditPollView(TemplateView):
    template_name = 'edit.html'

    def get_context_data(self, poll_id=-1, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = Poll.objects.filter(id=poll_id)

        if poll.count():
            poll = poll[0]
            context['page_title'] = f'Опрос № {poll_id}'
        else:
            poll = Poll()
            context['page_title'] = 'Новый опрос'

        # context['answers'] = AnswersForm(instance=Question.objects.filter(id=4)[0].answers)
        context['poll_id'] = poll.pk
        context['poll_form'] = PollForm(instance=poll)
        context['question_empty_form'] = QuestionForm
        questions_query_set = Question.objects.filter(poll=poll)
        questions = []
        for q in questions_query_set:
            questions.append({"question_form": QuestionForm(instance=q), "answers": AnswerFormSet(instance=q)})
        context['questions'] = questions
        return context

    def post(self, request, poll_id, **kwargs):
        if poll_id:
            user = request.user
            poll = Poll.objects.get(id=poll_id)
            if request.method == 'POST':
                form = PollForm(request.POST, instance=poll)
                if form.is_valid():
                    form.save()

            # TODO post form`
            # poll = Poll.objects.filter(id=poll_id)[0]
            # old_questions = Question.objects.filter(poll=poll)
            # if old_questions.count():
            #     for old_question in old_questions:
            #         old_question.delete()
        # else:
        #     poll = Poll()
        #     poll.date_of_begin = datetime.strftime(
        #         datetime.strptime(request.POST.get('date_of_begin'), '%d-%m-%Y'), '%Y-%m-%d')
        # poll.title = request.POST.get('title')
        # poll.description = request.POST.get('description')
        # poll.date_of_end = datetime.strftime(datetime.strptime(request.POST.get('date_of_end'), '%d-%m-%Y'), '%Y-%m-%d')
        # poll.save()
        # questions = json.loads(request.POST.get('questions'))
        # if questions:
        #     for every_question, question_info in questions.items():
        #         question = Question()
        #         question.answer_type = question_info.get('answer_type')
        #         question.text = question_info.get('text')
        #         question.poll = poll
        #         question.save()

        context = self.get_context_data(message='Poll added',
                                        poll_id=poll_id)
        return self.render_to_response(context)


def logout_view(request):
    logout(request)
    return redirect('/')
