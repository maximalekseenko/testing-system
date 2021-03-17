from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404
from django.core import serializers

import json

from static.py.view import get_base_context
from .form import ModuleForm
from .models import Task, Module
from main.models import Group


def CreateModuleView(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/register/")

    # context
    context = get_base_context(request, 'Создание Модуля', 'Создать')
    context['action'] = "create"
    context['form'] = ModuleForm({
            'name':              request.POST.get('name', ""),
            'author':            request.user,
            'assigned_to_value': request.POST.get('assigned_to_value', ""),
            'tasks_value':       request.POST.get('tasks_value', "[]"),
            'is_active':         request.POST.get('is_active', False),
            'is_public':         request.POST.get('is_public', False),
    })

    # POST
    if request.method == 'POST':
        form = context['form']

        # is valid
        if len(Module.objects.filter(name=form.data['name'])):
            return redirect(f'/tasks/create/')
            
        # create
        context['module'] = Module.objects.create(
            name      = form.data['name'],
            author    = form.data['author'],
            is_active = form.data.get('is_active', False)=="on",
            is_public = form.data.get('is_public', False)=="on",
        )
        context['module'].assigned_to.set(Group.objects.filter(name__in=form.data['assigned_to_value'].split('\r\n')))
        context['module'].tasks.all().delete()
        for task in json.loads(form.data['tasks_value']):
            new_task = Task.objects.create(
                name = task['name'],
                content = task['content'],
                answer = task['answer'],
                options = task['options'],
            )
            context['module'].tasks.add(new_task)
        # save
        context['module'].save()
        id = context['module'].id
        return redirect(f'/tasks/{id}/')
    # POST-end

    return render(request, 'module.html', context)
#CreateModuleView-end


def ShowModuleView(request, id):
    # is auth
    # if not request.user.is_authenticated:
    #     return redirect("/accounts/register/")
    # context
    context = get_base_context(request, 'Просмотр модуля', 'Сохравнить')
    try: context['module'] = Module.objects.get(id=id) 
    except Task.DoesNotExist: raise Http404
    context['action'] = "edit" if context['module'].author == request.user else "show"
    context['form'] = ModuleForm({
            'name':              request.POST.get('name', context['module'].name),
            'author':            request.POST.get('author', context['module'].author),
            'assigned_to_value': request.POST.get('assigned_to_value', "\n".join(map(lambda g: g.name, context['module'].assigned_to.all()))),
            'tasks_value':       request.POST.get('tasks_value', serializers.serialize('json', context['module'].tasks.all())),
            'is_active':         request.POST.get('is_active', context['module'].is_active),
            'is_public':         request.POST.get('is_public', context['module'].is_public),
    })

    # POST
    if request.method == 'POST':
        form = context['form']

        if form.data['tasks_value'][:4] == "RES-":
            form.data['tasks_value'] = form.data['tasks_value'][4:]
            if context['module'].marks.all().filter(user=request.user).count():
                context['module'].marks.all().get(user=request.user).note=form.data['tasks_value']
            else:
                context['module'].marks.all().create(user=request.user,note=form.data['tasks_value'])
        #RES-end

        if Module.objects.get(id=id).author != request.user:
            return redirect(f"/tasks/{id}")
        #IF AUTHOR-end
        if form.data['tasks_value'][:4] == "DEL-":
            form.data['tasks_value'] = form.data['tasks_value'][4:]
            context['module'].delete()
            return redirect(f'/tasks/')
        #DEL-end
        form.data['tasks_value'] = form.data['tasks_value'][4:]
        if len(Module.objects.filter(name=form.data['name'])) and form.data['name']!=context['module'].name:
            return render(request, 'module.html', context)
            
        context['module'].name      = form.data['name']
        context['module'].is_active = form.data.get('is_active', False)=="on"
        context['module'].is_public = form.data.get('is_public', False)=="on"
        context['module'].assigned_to.set(Group.objects.filter(name__in=form.data['assigned_to_value'].split('\r\n')))
        context['module'].tasks.all().delete()
        for task in json.loads(form.data['tasks_value']):
            new_task = Task.objects.create(
                name = task['name'],
                content = task['content'],
                answer = task['answer'],
                options = task['options'],
            )
            context['module'].tasks.add(new_task)
            
        context['module'].save()
        return redirect(f'/tasks/{id}/')
        #NEW-del
    # POST-end

    return render(request, 'module.html', context) 
#ShowModuleView-end
