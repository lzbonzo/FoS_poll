from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path

from fos_poll import views

urlpatterns = [
    path("about/", views.About.as_view(), name='about'),
    path("", views.PollListView.as_view(template_name='index.html'), name='main_page'),
    path("poll/<int:pk>", views.UserPollView.as_view(), name='poll'),
    path("admin/", views.AdminPollListView.as_view(), name='admin'),
    path("admin/edit/<int:pk>/", views.EditPollView.as_view(), name='edit'),
    path("admin/new_poll", views.EditPollView.as_view(), name='new_poll'),
    path("my_polls/", views.MyPollsView.as_view(), name='my_polls'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    path("api/v0/new_poll/", views.EditPollApiView.as_view(), name='api_new_poll'),
    path("api/v0/poll/<int:poll_id>/", views.EditPollApiView.as_view(), name='api_poll_data'),
    path("api/v0/polls/", views.EditPollApiView().as_view(), name='api_polls_list'),
    path("api/v0/logout/", views.ApiLogoutView.as_view(), name='api_logout'),
    path("api/v0/login/", views.ApiLoginView.as_view(), name='api_login'),
]
