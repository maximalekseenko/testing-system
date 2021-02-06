from django.contrib.auth.models import User
from django.shortcuts import render

def HomeView(request):
    user = request.user
    args={"user": user}
    return render(request, 'home.html', args)

def HeresyoneView(request):

    args={
        "TEST" : "TEST",
    }

    return render(request, 'heresypage1.html', args)