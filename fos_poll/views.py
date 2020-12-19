from collections import OrderedDict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import TemplateView

from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from fos_poll.models import Poll, Question
from fos_poll.forms import QuestionFormSet, PollForm, QuestionForm
from fos_poll.permissions import IsAdminOrReadOnly
from fos_poll.serializers import PollSerializer


class EditPollApiView(APIView):
    """
        CRUD API methods
    """
    permission_classes = (IsAdminOrReadOnly, )

    def get(self, request, poll_id=None):
        if not poll_id:
            polls = Poll.objects.all()
            polls_data = PollSerializer(polls, many=True).data
            for poll in polls_data:
                poll['questions'] = len(poll['questions'])
            return Response({"poll": polls_data})

        poll = Poll.objects.get(id=poll_id)
        poll_serializer = PollSerializer(poll)
        return Response({"poll": poll_serializer.data})

    def post(self, request):
        poll = request.data.get('poll')
        poll_serializer = PollSerializer(data=poll)
        if poll_serializer.is_valid(raise_exception=True):
            poll_saved = poll_serializer.save()
        return Response(f'"success": "Poll "{poll_saved.id}" created successfully"')

    def put(self, request, poll_id):
        poll_data = request.data.get('poll')
        saved_poll = get_object_or_404(Poll.objects.all(), id=poll_id)
        poll_serializer = PollSerializer(instance=saved_poll, data=poll_data, partial=True)
        if poll_serializer.is_valid(raise_exception=True):
            poll_serializer.update(saved_poll, poll_data)
        return Response(f'"success": "Poll {poll_id} update successfully"')

    def delete(self, request, poll_id):
        poll = get_object_or_404(Poll.objects.all(), id=poll_id)
        poll.delete()
        return Response({
              f'"message": "Poll with id {poll_id} has been deleted."'
        }, status=204)


class UserPollApiView(APIView):
    pass


class About(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'about'
        return context


class MainPageView(generic.ListView):
    template_name = 'index.html'
    model = Poll


class UserPollView(generic.DetailView):
    template_name = 'poll.html'
    model = Poll
    form_class = PollForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = context['poll']
        context['questions_formset'] = QuestionFormSet(prefix='questions_formset', instance=poll)
        return context


class AdminLoginView(LoginView):
    template_name = 'login.html'

    def post(self, request, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')
        else:
            context = super().get_context_data(**kwargs)
            context['message'] = '*логин или пароль введены неверно'
            return render(request, self.template_name, context)


class UserLogoutView(LogoutView):
    pass


class AdminPollsView(generic.ListView):
    permission_classes = (permissions.IsAdminUser,)
    template_name = 'admin.html'
    model = Poll

    def post(self, request):
        Poll.objects.get(pk=request.POST.get('id')).delete()
        self.object_list = self.get_queryset()
        return HttpResponseRedirect('/')


class MyPollsView(TemplateView):
    template_name = 'my_polls.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        polls = Poll.objects.values('title', 'description', 'id')
        context['polls'] = polls
        return context


class EditPollView(generic.UpdateView):
    template_name = 'edit.html'
    model = Poll
    form_class = PollForm
    success_url = '/admin/'

    def get_object(self, queryset=None):
        """ Return new Poll.object On create or object from db on update"""
        if self.kwargs.get('pk'):
            return super().get_object()
        return Poll()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = context['poll']
        context['questions_formset'] = QuestionFormSet(prefix='questions_formset', instance=poll)
        return context

    def post(self, request, *args, **kwargs):
        super_post = super().post(request, *args, **kwargs)
        poll = self.object

        questions = self.serialize_data(request.POST)
        Question.objects.filter(poll=poll).delete()
        for question, data in questions.items():
            question_form = QuestionForm(instance=Question(poll=poll), data=data)
            if question_form.is_valid():
                question_form.save()
        return super_post

    def serialize_data(self, post_data):
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
                        questions[question]['answers'].append({'text': value, 'is_right': True})
                    elif field_name == 'isRight':
                        is_right_list.extend(post_data.getlist(field))
                    else:
                        if 'answerOption' in field_name:
                            questions[question]['answers'].append({'text': value, 'is_right': False})
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
