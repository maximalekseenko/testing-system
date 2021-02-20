from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404

from static.py.view import get_base_context
from .form import   AddTaskForm,    ModuleForm
from .models import Task,           Module
from main.models import Group


def CreateModuleView(request):  
    if not request.user.is_authenticated:
        return redirect("/accounts/register/")

    context = get_base_context(request, 'Создание Модуля', 'Создать')
    context['action'] = "create"
    
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if len(Module.objects.filter(name=form.data['name'])):
            return redirect('/tasks/create/')
        #create new module
        new_module = Module(
            name   = form.data['name'],
            author = request.user,
        )
        new_group.members.set(User.objects.filter(username__in=form.data['members'].split('\r\n')))
        #save new module
        new_module.save()
        #show new module
        id = new_module.id
        return redirect(f'/tasks/{id}/')
    #if POST-end
    context['form'] = ModuleForm(
        initial={
            'name':         "",
            'author':       request.user,
            'assigned_to':  "",
            'tasks':        "",
        } )
    context['all_groups'] = Group.objects.all()
    # context['members']   = request.user
    return render(request, 'module.html', context)
#CreateModuleView-end


def ShowGroupView(request, id):
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


def ShowModuleView(request, id):
    context = get_base_context(request, 'show Module')
    try:
        context['module'] = Module.objects.get(id=id)
    except Task.DoesNotExist:
        raise Http404
    #try find module-end
    if request.method == 'POST':
        if context['user'] == context['module'].author:
            return redirect(f'/tasks/{id}/edit')
        else:
            return redirect(f'/tasks/{id}/do')
    #if POST-end
    return render(request, 'showmodule.html', context) 
#ShowModuleView-end


def EditModuleView(request, id):
    context = get_base_context(request, 'Edit Module')
    try:
        context['module'] = Module.objects.get(id=id)
    except Task.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        if context['user'] == context['module'].author:
            return redirect(f'/tasks/{id}/edit')
        else:
            return redirect(f'/tasks/{id}/do')
    return render(request, 'editmodule.html', context) 
#EditModuleView-end


    # #task
    # path('tasks/<int:id>/create/',       tasks.CreateTaskView),
    # path('tasks/<int:id>/<int:id>/',     tasks.ShowTaskView),


def CreateTaskView(request):
    context = get_base_context(request, 'Добавление нового задания')
    if request.method == 'POST':
        addform = AddTaskForm(request.POST)
        if addform.is_valid():
            new_task = Task(
                user=request.user,
                name=addform.data['name'],
                content=addform.data['content'],
                # creation_date=datetime.datetime.now(),
            )
            new_task.save()
            Module.objects.get(id=int(addform.data['module'])).tasks.add(new_task)
            id = new_task.id
            # messages.add_message(request, messages.SUCCESS, "Задание успешно добавлено")
            return redirect(f'/show/{id}/')
        else:
            # messages.add_message(request, messages.ERROR, "Некорректные данные в форме")
            return redirect('create/')
    else:
        context['addform'] = AddTaskForm(
            initial={
                'user': request.user,
            }
        )
    context['all_modules'] = Module.objects.all()
    return render(request, 'createtask.html', context)


def EditTaskView(request):
    if request.user.userprofile.user_type != "teacher":
        return redirect('/accounts/')
    if request.method == "POST":
        task = Task(name=request.POST.get("name"), content=request.POST.get("content"))
        task.save()
        return redirect('/')
    return render(request, 'showtask.html')


def ShowTaskView(request, id):
    context = get_base_context(request, 'Просмотр задания')
    try:
        show_task = Task.objects.get(id=id)
        context['addform'] = AddTaskForm(
            initial={
                'user': show_task.user if show_task.user else 'AnonymousUser',
                'name': show_task.name,
                'content': show_task.content,
            }
        )
    except Task.DoesNotExist:
        raise Http404
    return render(request, 'showtask.html', context) 

