from django.shortcuts import render, redirect
from static.py.view import get_base_context, is_user_authenticated, get_new_key
from .models import Group
# json
import json
from django.core import serializers
# errors
from django.db.utils import IntegrityError
from django.http import Http404

#to be anihilated
from django.contrib.auth.models import User
from .form import GroupForm


def HomeView(request): pass
def InviteView(request): pass

def CreateView(request):
    if not is_user_authenticated(request):
        return redirect("/accounts/register/groups_create/")

    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        return render(request, 'group_create.html', context)

    # scrap data
    name        = request.POST['name']
    description = request.POST['description']
    author      = request.user
        
    # creation
    try: new_group = Group.objects.create(
            name        = name,
            author      = author,
            description = description,
            id          = get_new_key())
    except IntegrityError: pass

    # save
    new_group.save()  
    
    # proceed
    return redirect(f'/groups/{new_group.id}/')
# CreateGroupView - end


def ShowView(request, id):
    # does id exist
    try: cur_group = Group.objects.get(id=id)
    except Group.DoesNotExist: raise Http404
        
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        context['group'] = cur_group
        return render(request, 'group_show.html', context)
    
    # what request
    if "btn_mem" in request.POST:
        return redirect(f'/groups/{id}/users/')
    if "btn_edit" in request.POST:
        return redirect(f'/groups/{id}/edit/')
    if "btn_join" in request.POST:
        return redirect(f'/groups/{id}/join/')
# ShowView - end


def EditView(request, id):
    # does id exist
    try: cur_group = Group.objects.get(id=id)
    except Group.DoesNotExist: raise Http404

    # is user author 
    if cur_group.author != request.user: raise Http404
        
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        context['group'] = cur_group
        return render(request, 'group_edit.html', context)
    
    # cancel
    if "cancel_btn" in request.POST:
        return redirect(f'/groups/{id}/')

    # delete module
    if 'btn_del' in request.POST:
        cur_group.delete()
        return redirect(f'/')

    # scrap data
    name            = request.POST['name']
    description     = request.POST['description']

    # save module
    if 'btn_save' in request.POST:
        cur_group.name = name
        cur_group.description = description
        cur_group.save()
        return redirect(f'/groups/{id}/') 
# EditView - end


def MembersView(request, id):
    # does id exist
    try: cur_group = Group.objects.get(id=id)
    except Group.DoesNotExist: raise Http404

    # is user author 
    if cur_group.author != request.user: raise Http404
        
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        context['group'] = cur_group
        return render(request, 'group_members.html', context)
# MembersView - end


def JoinView(request, id):
    # does id exist
    try: cur_group = Group.objects.get(id=id)
    except Group.DoesNotExist: raise Http404

    # is not user author 
    if cur_group.author == request.user: raise Http404
    
    print(cur_group.members.all())
    if request.user in cur_group.members.all(): raise Http404
    if request.user in cur_group.members_pending.all(): raise Http404

    print("DIE SCUM")

    cur_group.members_pending.add(request.user)
    cur_group.save()

    return redirect(f'/groups/{id}/') 