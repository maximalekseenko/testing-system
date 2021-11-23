from django.shortcuts import render, redirect
from tasks.models import Module
from groups.models import Group


def get_base_context(request, pagename, buttonname=""):
    context = {}
    context['pagename']    = pagename
    context['buttonname']  = buttonname
    context['user']        = request.user
    context['all_modules'] = Module.objects.filter(is_public=True, is_active=True)


    if request.user.is_authenticated:
        # context['group-module_dic'] = {group:module Group.objects.filter(author__id=request.user.id)}
        # context['modules_groups'] = {group:set(Module.objects.filter(is_active=True, assigned_to=group)) for group in Group.objects.filter(members__id=request.user.id)}

        context['my_modules']     = Module.objects.filter(author=request.user)
        context['my_groups']      = Group.objects.filter(author__id=request.user.id)
        context['modules_groups'] = {group:set(Module.objects.filter(is_active=True, assigned_to=group)) for group in Group.objects.filter(members__id=request.user.id)}

    return context