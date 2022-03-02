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
    path('accounts/register/',              accounts.RegisterView),
    path('accounts/logout/',                LogoutView.as_view()),
    path('accounts/',                       accounts.AccoutView),
#groups
    path('groups/create/',                  groups.CreateView),
    path('groups/',                         groups.ShowView),
    path('groups/edit/',                    groups.EditView),
    path('groups/moduls/',                  groups.ModulsView),
    path('groups/moduls/results/',          groups.ModulesResultsView),
    path('groups/members/',                 groups.MembersView),
    path('groups/join/',                    groups.JoinView),
#tasks
    path('tasks/create/',                   tasks.CreateView),
    path('tasks/',                          tasks.ShowView),
    path('tasks/edit/',                     tasks.EditView),
    path('tasks/edit/task/',                tasks.EditTaskView),
    path('tasks/pass/',                     tasks.PassView),
    path('tasks/result/',                   tasks.ResultView),
#main
    path('' ,                               main.HomeView),

]
