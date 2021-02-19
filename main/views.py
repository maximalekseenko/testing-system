from django.shortcuts import render, redirect
from static.py.view import get_base_context


def HomeView(request):
    context = get_base_context(request, "Главная страница")
    return render(request, 'home.html', context)
#HomeView-end


def ListGroupView(request):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)
#ListGroupView-end


def CreateGroupView(request):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)
#CreateGroupView-end


def ShowGroupView(request, id):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)
#ShowGroupView-end


def EditGroupView(request, id):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)
#HomEditGroupVieweView-end
