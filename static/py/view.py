from django.shortcuts import render, redirect
from tasks.models import Module
from main.models import Group

def get_base_context(request, pagename):
    is_auth = request.user.is_authenticated
    return {
        'my_modules'        : Module.objects.filter(author=request.user) if is_auth else [],
        'active_modules'    : Module.objects.filter(is_active=True, assigned_to__members__id=request.user.id) if is_auth else [],
        'all_modules'       : Module.objects.filter(is_active=True),
        'my_groups'         : Group.objects.filter(members__id=request.user.id) if is_auth else [],
        'pagename'          : pagename,
        'user'              : request.user,
    }