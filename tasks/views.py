from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404

from static.py.view import get_base_context
from .form import   AddTaskForm,    ModuleForm
from .models import Task,           Module
from main.models import Group


def CreateModuleView(request):  
    # is auth
    if not request.user.is_authenticated:
        return redirect("/accounts/register/")
    # context
    context = get_base_context(request, 'Создание Модуля', 'Создать')
    context['action'] = "create"
    context['form'] = ModuleForm({
            'name':         request.POST.get('name', ""),
            'author':       request.user,
            'assigned_to':  request.POST.get('assigned_to', ""),
            'tasks':        request.POST.get('tasks', ""),
            'is_active':    request.POST.get('is_active', False)!=False,
            'is_public':    request.POST.get('is_public', False)!=False,
        } )
    # POST
    if request.method == 'POST':
        form = context['form']
        # is valid
        if len(Module.objects.filter(name=form.data['name'])):
            return render(request, 'module.html', context)
        # create new module
        new_module = Module.objects.create(
            name        = form.data['name'],
            author      = form.data['author'],
            is_active   = form.data.get('is_active', False)!=False,
            is_public   = form.data.get('is_public', False)!=False,
        )
        new_module.assigned_to.set(Group.objects.filter(name__in=form.data['assigned_to'].split('\r\n')))
        # save and show new module
        new_module.save()
        id = new_module.id
        return redirect(f'/tasks/{id}/')
    # POST-end
    return render(request, 'module.html', context)
#CreateModuleView-end


def ShowModuleView(request, id):
    # is auth
    if not request.user.is_authenticated:
        return redirect("/accounts/register/")
    # context
    context = get_base_context(request, 'Просмотр модуля', 'Сохравнить')
    try:    # FIX: to one line pls
        context['module'] = Module.objects.get(id=id)
    except Task.DoesNotExist:
        raise Http404
    context['action'] = "edit" if context['module'].author == request.user else "show"
    context['form'] = ModuleForm({ # FIX: len of line
            'name':         request.POST.get('name', context['module'].name),
            'author':       request.POST.get('author', context['module'].author),
            'assigned_to':  request.POST.get('assigned_to', "\r\n".join(map(lambda g: g.name, context['module'].assigned_to.all()))),
            'tasks':        request.POST.get('tasks', "\r\n".join(map(lambda g: g.name, context['module'].assigned_to.all()))),
            'is_active':    request.POST.get('is_active', context['module'].is_active)!=False,
            'is_public':    request.POST.get('is_public', context['module'].is_public)!=False,
        } )
    # POST
    if request.method == 'POST':
        form = context['form']
        # is not owner
        if Module.objects.get(id=id).author != request.user:
            return redirect(f"/tasks/{id}")
        # is valid
        if len(Module.objects.filter(name=form.data['name'])) and form.data['name'] != context['module'].name:
            return render(request, 'module.html', context)
        # edit
        context['module'].name      = form.data['name']
        context['module'].is_active = form.data.get('is_active', False)!=False
        context['module'].is_public = form.data.get('is_public', False)!=False
        context['module'].assigned_to.set(Group.objects.filter(name__in=form.data['assigned_to'].split('\r\n')))
        # save
        context['module'].save()
        return redirect(f'/tasks/{id}/')
    # POST-end

    return render(request, 'module.html', context) 
#ShowModuleView-end


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

