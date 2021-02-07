from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('heresyone/', views.HeresyoneView),
    url('taskcreation/', views.CreateTaskView),
    url('taskedition/', views.EditTaskView),
    url('showtask/<int:id>', views.ShowTaskView, name='view_task'),
    url('', views.HomeView),
]