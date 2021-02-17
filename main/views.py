from django.shortcuts import render, redirect
from static.py.view import get_base_context


def HomeView(request):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)
