from django.shortcuts import render, redirect
from static.py.view import get_base_context, is_user_registred, get_new_key
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from .models import Group
from .form import GroupForm
import json

def HomeView(request): pass
def InviteView(request): pass

def CreateView(request):
    if not is_user_registred(request):
        return redirect("/accounts/register/")

    context = get_base_context(request, 'Создание группы', 'Создать')
    
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        if len(Group.objects.filter(name=name, author=request.user)):
            return redirect('/groups/create/')
        try:
            new_group = Group.objects.create(
                name   = name,
                author = request.user,
                description = description,
                id = get_new_key()
            )
        except IntegrityError: pass
        new_group.save()  
        id = new_group.id  
        return redirect(f'/groups/{id}/')
    #if POST-end
    return render(request, 'group_create.html', context)
#CreateGroupView-end


def ShowView(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/register/")
        
    context = get_base_context(request, 'Просмотр группы', 'Сохравнить')
    #get group
    try:
        context['group'] = Group.objects.get(id=id)
    except Task.DoesNotExist:
        raise Http404

    context['action'] = "edit" if context['group'].author == request.user else "show"
    
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
    context['form'] = GroupForm(initial={
            'name'      : context['group'].name,
            'author'    : context['group'].author,
            'members'   : "\r\n".join(map(str, context['group'].members.all())),
        } )
    context['all_users']    = User.objects.all()
    context['members']      = " ".join(list(map(lambda m: m.username, context['group'].members.all())))
    return render(request, 'group.html', context)
#ShowGroupView-end