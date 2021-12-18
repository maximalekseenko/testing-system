from django.shortcuts import render, redirect
from static.py.view import get_base_context
from django.contrib.auth.models import User
import json

def HomeView(request):
    context = get_base_context(request)
    return render(request, 'home.html', context)
#HomeView-end