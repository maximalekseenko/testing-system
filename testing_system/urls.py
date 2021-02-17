from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
import  main.views      as  main,\
        accounts.views  as  accounts,\
        tasks.views     as  tasks


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # accounts
    path('accounts/login/',     LoginView.as_view()),
    path('accounts/logout/',    LogoutView.as_view()),
    path('accounts/register/',  accounts.RegisterView),
    path('accounts/',           accounts.AccoutView),
    # tasks
    url(r'^tasks/', include('tasks.urls')),
    # main
    path('' ,                   main.HomeView),
    ]
