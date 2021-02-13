from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def get_base_context(request, pagename):
    return {
        'pagename': pagename,
        'user': request.user,
    }


def HomeView(request):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)


def HeresyoneView(request):
    context = get_base_context(request, "ы")
    return render(request, 'heresypage1.html', context)

