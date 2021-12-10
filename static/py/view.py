from django.shortcuts import render, redirect
from tasks.models import Module
from groups.models import Group
from string import ascii_letters, digits, punctuation
from random import sample


def get_new_key(length=16):
    all = ascii_letters + digits + punctuation
    return "".join(sample(all,length))


def is_user_pure_for_page(request):
    if not request.user.is_authenticated: return False
    return True

def is_user_registred(request):
    if not request.user.is_authenticated: return False
    return True

def is_user_authenticated(request):#fix
    if not request.user.is_authenticated: return False
    return True

def get_base_context(request, pagename, buttonname=""):
    context = {}
    context['pagename']    = pagename
    context['buttonname']  = buttonname
    context['user']        = request.user
    context['all_modules'] = Module.objects.filter(is_public=True, is_active=True)


    if request.user.is_authenticated:
        context['my_groups']      = [[group, getattr(group,'moduls').count()] for group in Group.objects.filter(members__id=request.user.id)]
        context['new_modules']    = Module.objects.filter(author=request.user)
    return context