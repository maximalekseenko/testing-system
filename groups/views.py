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

    # validation
    if len(Group.objects.filter(name=name, author=author)):
        return redirect('/groups/create/')
        
    # creation
    try:
        new_group = Group.objects.create(
            name        = name,
            author      = author,
            description = description,
            id          = get_new_key()
        )
    except IntegrityError: pass

    # save
    new_group.save()  
    
    # proceed
    return redirect(f'/groups/{new_group.id}/')
# CreateGroupView - end


def ShowView(request, id):
    if not is_user_authenticated(request):
        return redirect(f"/accounts/register/groups_{id}")
        
    context = get_base_context(request)
    
    #get group
    try:
        context['group'] = Group.objects.get(id=id)
    except Group.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        #is not owner
        if context['action'] != "edit":
            return redirect(f"/groups/{id}")

        #get data form POST
        form = GroupForm(request.POST)
        if len(Group.objects.filter(name=form.data['name'])) and Group.objects.filter(name=form.data['name'])[0].name != context['group'].name:
            return redirect('/groups/create/')

        # if delete
        if not form.data.get('members',""):
            context['group'].delete()
            return redirect('/')
        #save edited group
        context['group'].name   = form.data['name']
        context['group'].members.set(User.objects.filter(username__in=form.data['members'].split('\r\n')))
        context['group'].save()
        return redirect(f'/groups/{id}/')
    #if POST-end
    
    if context['group'].author == request.user: context["gr_action"] = "edit"
    elif not context['group'].members.contains(request.user): context["gr_action"] = "join"
    return render(request, 'group_show.html', context)
# ShowGroupView - end
