from django.contrib.auth.models import User
from django.shortcuts import render
from .models import test1

def HomeView(request):
    user_data = User.objects.get(username=request.user).UserProfile
    args={"user_data": user_data}
    return render(request, 'home.html', args)

def HeresyoneView(request):
    test = test1.objects.first()

    args={
        "test" : test,
        "TEST" : "TEST",
    }

    return render(request, 'heresypage1.html', args)