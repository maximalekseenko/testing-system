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
        new_module = Module.objects.create(
            name        = form.data['name'],
            author      = request.user,
            is_active   = form.data.get('is_active', False)!=False,
            is_public   = form.data.get('is_public', False)!=False,
        )
        # new_module.tasks.set(Task.objects.filter(name__in=form.data['tasks'].split('\r\n')))
        new_module.assigned_to.set(Group.objects.filter(name__in=form.data['assigned_to'].split('\r\n')))
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
            'is_active':    True,
            'is_public':    False,
        } )
    context['assigned_to'] = ""
    return render(request, 'module.html', context)
#CreateModuleView-end


def ShowModuleView(request, id):
    if not request.user.is_authenticated:
        return redirect("/accounts/register/")
    context = get_base_context(request, 'Просмотр модуля', 'Сохравнить')
    #get module
    try:
        context['module'] = Module.objects.get(id=id)
    except Task.DoesNotExist:
        raise Http404
    context['action'] = "edit" if context['module'].author == request.user else "show"
    if request.method == 'POST':
        #is not owner
        if context['action'] != "edit":
            return redirect(f"/tasks/{id}")
        #get data form POST
        form = ModuleForm(request.POST)
        if len(Module.objects.filter(name=form.data['name'])) and Module.objects.filter(name=form.data['name'])[0].name != context['module'].name:
            return redirect('/module/create/')
        context['module'].name      = form.data['name']
        context['module'].is_active = form.data.get('is_active', False)!=False
        context['module'].is_public = form.data.get('is_public', False)!=False
        context['module'].assigned_to.set(Group.objects.filter(name__in=form.data['assigned_to'].split('\r\n')))
        #save edited group
        context['module'].save()
        return redirect(f'/tasks/{id}/')
    context['form'] = ModuleForm(
        initial={
            'name':         context['module'].name,
            'author':       context['module'].author,
            'assigned_to':  "\r\n".join(map(lambda g: g.name, context['module'].assigned_to.all())),
            'tasks':        "\r\n".join(map(lambda g: g.name, context['module'].assigned_to.all())),
            'is_active':    context['module'].is_active,
            'is_public':    context['module'].is_public,
        } )
    context['all_groups']    = User.objects.all()
    context['assigned_to']   = " ".join(list(map(lambda m: m.name, context['module'].assigned_to.all())))
    #if POST-end
    return render(request, 'module.html', context) 
#ShowModuleView-end


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

