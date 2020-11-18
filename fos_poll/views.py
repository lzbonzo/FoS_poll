from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.views.generic import TemplateView

from fos_poll.models import Poll, Question
from fos_test import settings


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
        print(request.POST)
        # Poll.objects.get(id=5).delete()
        return self.render_to_response(context)


class MyPollsView(TemplateView):
    template_name = 'my_polls.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls = Poll.objects.values('title', 'description')
        context['polls'] = polls
        return context


class EditPollView(TemplateView):
    template_name = 'edit.html'

    def get_context_data(self, poll_id, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = Poll.objects.filter(id=poll_id)[0]
        question = Question()._meta.get_field('answer_type').choices

        context['id'] = poll.id
        context['title'] = poll.title
        context['description'] = poll.description
        context['date_of_begin'] = datetime.strftime(poll.date_of_begin, '%d-%m-%Y')
        context['date_of_end'] = datetime.strftime(poll.date_of_end, '%d-%m-%Y')
        context['question'] = question

        return context


def logout_view(request):
    logout(request)
    return redirect('/')
