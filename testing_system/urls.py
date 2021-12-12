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
    path('accounts/login/',             accounts.LoginView),
    path('accounts/login/<str:red>/',   accounts.LoginView),
    path('accounts/register/<str:red>/',accounts.RegisterView),
    path('accounts/register/',          accounts.RegisterView),
    path('accounts/logout/',            LogoutView.as_view()),
    path('accounts/',                   accounts.AccoutView),
#groups
    path('groups/',                     groups.HomeView),
    path('groups/create/',              groups.CreateView),
    path('groups/<str:id>/',            groups.ShowView),
#tasks
    path('tasks/',                      tasks.FindModuleView),
    path('tasks/create/',               tasks.CreateModuleView),
    path('tasks/<int:id>/',             tasks.ShowModuleView),
#main
    path('' ,                           main.HomeView),

]
