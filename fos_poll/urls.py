from django.urls import path

from fos_poll import views


urlpatterns = [
    path("about/", views.About.as_view(), name='about'),

]
