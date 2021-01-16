from django.conf.urls import url, include
from main.views import HomeView

urlpatterns = [
    url('', HomeView),
]