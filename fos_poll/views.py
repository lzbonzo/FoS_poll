import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from fos_poll.models import Poll, Question


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
        current_poll_data = {}
        poll = Poll.objects.filter(id=poll_id)
        if poll.count():
            poll = poll[0]
            current_poll_data['title'] = poll.title
            current_poll_data['description'] = poll.description
            current_poll_data['date_of_begin'] = datetime.strftime(poll.date_of_begin, '%d-%m-%Y')
            current_poll_data['date_of_end'] = datetime.strftime(poll.date_of_end, '%d-%m-%Y')
            current_poll_data['id'] = poll.id
            questions = Question.objects.filter(poll=poll)
            current_poll_data['questions'] = questions

        answer_types = Question()._meta.get_field('answer_type').choices
        current_poll_data['answer_types'] = answer_types
        context['poll'] = current_poll_data
        return context

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')

        print('id',id)
        if id:
            poll = Poll.objects.filter(id=id)[0]
            old_questions = Question.objects.filter(poll=poll)
            if old_questions.count():
                for old_question in old_questions:
                    old_question.delete()
        else:
            poll = Poll()
            poll.date_of_begin = datetime.strftime(
                datetime.strptime(request.POST.get('date_of_begin'), '%d-%m-%Y'), '%Y-%m-%d')
        poll.title = request.POST.get('title')
        poll.description = request.POST.get('description')
        poll.date_of_end = datetime.strftime(datetime.strptime(request.POST.get('date_of_end'), '%d-%m-%Y'), '%Y-%m-%d')
        poll.save()
        questions = json.loads(request.POST.get('questions'))
        if questions:
            for every_question, question_info in questions.items():
                question = Question()
                question.answer_type = question_info.get('answer_type')
                question.text = question_info.get('text')
                question.poll = poll
                question.save()

        context = self.get_context_data(message='Poll added',
                                        poll_id=poll.id)
        return self.render_to_response(context)


def logout_view(request):
    logout(request)
    return redirect('/')
