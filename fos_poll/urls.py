from django.urls import path

from fos_poll import views


urlpatterns = [
    path("about/", views.About.as_view(), name='about'),
    path("", views.MainPageView.as_view(), name='main_page'),
    path("poll<int:poll_id>", views.PollView.as_view(), name='poll'),
    path("login/", views.AdminLoginView.as_view(), name='login'),
    path("admin/", views.AdminPollsView.as_view(), name='admin'),
    path("admin/<int:poll_id>", views.EditPollView.as_view(), name='edit'),
    path("admin/new_poll", views.EditPollView.as_view(), name='new_poll'),
    path("my_polls/", views.MyPollsView.as_view(), name='my_polls'),
    path("my_polls/poll<int:poll_id>", views.PollView.as_view(), name='my_polls'),
    path("logout/", views.logout_view, name='logout'),
]
