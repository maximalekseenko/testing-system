from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    url('heresyone/', views.HeresyoneView),
    url('', views.HomeView),
]