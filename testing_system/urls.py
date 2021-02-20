from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
import  main.views      as  main,\
        accounts.views  as  accounts,\
        tasks.views     as  tasks


urlpatterns = [
    path('admin/', admin.site.urls),
#accounts
    path('accounts/login/',             LoginView.as_view()),
    path('accounts/logout/',            LogoutView.as_view()),
    path('accounts/register/',          accounts.RegisterView),
    path('accounts/',                   accounts.AccoutView),
#tasks
    #module
    path('tasks/create/',               tasks.CreateModuleView),
    path('tasks/<int:id>/',             tasks.ShowModuleView),
    #task
    # path('tasks/<int:id>/create/',      tasks.CreateTaskView),
    # path('tasks/<int:id>/<int:AAA>/',    tasks.ShowTaskView),
#main
    #groups
    path('groups/create/',              main.CreateGroupView),
    path('groups/<int:id>/',            main.ShowGroupView),
    #home
    path('' ,                           main.HomeView),

]
