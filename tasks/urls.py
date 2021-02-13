from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    url('create/', views.CreateTaskView),
    url('edit/', views.EditTaskView),
    path('show/<int:id>/', views.ShowTaskView),
]