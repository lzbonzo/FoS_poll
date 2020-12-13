from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.
from django.views import generic
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework.views import APIView

from fos_poll.models import Poll, Question
from fos_poll.forms import QuestionFormSet, PollForm
from fos_poll.serializers import PollSerializer


class EditPollApiView(APIView):
    """
        API methods
    """
    permission_classes = (permissions.IsAdminUser,)

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


class PollView(generic.DetailView):
    template_name = 'poll.html'
    model = Poll


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = context['poll']
        context['questions_formset'] = QuestionFormSet(prefix='questions_formset', instance=poll)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect('main_page')
