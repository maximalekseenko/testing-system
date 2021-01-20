from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import RegisterView

urlpatterns = [
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^register/$', RegisterView),
]