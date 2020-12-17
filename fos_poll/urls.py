from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import auth_logout

from fos_poll import views

urlpatterns = [
    path("about/", views.About.as_view(), name='about'),
    path("", views.MainPageView.as_view(), name='main_page'),
    path("<int:pk>", views.UserPollView.as_view(), name='poll'),
    path("login/", views.AdminLoginView.as_view(), name='login'),
    path("admin/", views.AdminPollsView.as_view(), name='admin'),
    path("admin/<int:pk>", views.EditPollView.as_view(), name='edit'),
    path("admin/new_poll", views.EditPollView.as_view(), name='new_poll'),
    path("my_polls/", views.MyPollsView.as_view(), name='my_polls'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='logout'),

    path("api/v0/new_poll/", views.EditPollApiView.as_view(), name='api_new_poll'),
    path("api/v0/edit/<int:poll_id>/", views.EditPollApiView.as_view(), name='api_edit_poll'),
    path("api/v0/polls/", views.EditPollApiView().as_view(), name='api_polls_list'),
]
