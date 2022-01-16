from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
import  main.views      as main,\
        groups.views    as groups,\
        accounts.views  as accounts,\
        tasks.views     as tasks


urlpatterns = [
    path('admin/', admin.site.urls),
#accounts
    path('accounts/login/',                 accounts.LoginView),
    path('accounts/login/<str:red>/',       accounts.LoginView),
    path('accounts/register/<str:red>/',    accounts.RegisterView),
    path('accounts/register/',              accounts.RegisterView),
    path('accounts/logout/',                LogoutView.as_view()),
    path('accounts/',                       accounts.AccoutView),
#groups
    path('groups/',                         groups.HomeView),
    path('groups/create/',                  groups.CreateView),
    path('groups/<str:id>/',                groups.ShowView),
    path('groups/<str:id>/edit/',           groups.EditView),
    path('groups/<str:id>/join/',           groups.JoinView),
    path('groups/<str:id>/users/',          groups.MembersView),
#tasks
    path('tasks/',                          tasks.FindView),
    path('tasks/create/',                   tasks.CreateView),
    path('tasks/<str:id>/',                 tasks.ShowView),
    path('tasks/<str:id>/edit/',            tasks.EditView),
    path('tasks/<str:id>/edit/<int:tn>/',   tasks.EditTaskView),
    path('tasks/<str:id>/edit/<int:tn>/del/',tasks.DelTaskView),
    path('tasks/<str:id>/pass',             tasks.PassView),
#main
    path('' ,                               main.HomeView),

]
