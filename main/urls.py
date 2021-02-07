from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    url('heresyone/', views.HeresyoneView),
    url('taskcreation/', views.CreateTaskView),
    url('taskedition/', views.EditTaskView),
    path('showtask/<int:id>/', views.ShowTaskView),
    url('', views.HomeView),
]