from django.shortcuts import render, redirect
from static.py.view import get_base_context
from django.contrib.auth.models import User
from .models import Group
from .form import GroupForm

def HomeView(request):
    context = get_base_context(request, "Главная страница")
    return render(request, 'home.html', context)
#HomeView-end


def ListGroupView(request):
    context = get_base_context(request, "Группы")
    context['my_groups'] = Group.objects.filter(members__id=request.user.id)
    return render(request, 'listgroup.html', context)
#ListGroupView-end


def CreateGroupView(request):  
    print(request.POST)  
    context = get_base_context(request, 'Создание группы')

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if len(Group.objects.filter(name=form.data['name'])):
            return redirect('/groups/create/')
        new_group = Group.objects.create(
            name   = form.data['name'],
        )
        new_group.members.set(User.objects.filter(username__in=form.data['members'].split('\r\n')))
        new_group.save()

        # new_module.save()
        id = new_module.id
        return redirect(f'/tasks/{id}/')
    #if POST-end
    context['form'] = GroupForm(initial={
            'name':         "",
            'members':      request.user,
        } )
    context['all_users'] = User.objects.all()
    return render(request, 'creategroup.html', context)
#CreateGroupView-end


def ShowGroupView(request, id):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)
#ShowGroupView-end


def EditGroupView(request, id):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)
#HomEditGroupVieweView-end
