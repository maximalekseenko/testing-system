from django.shortcuts import render, redirect
from static.py.view import get_base_context, is_user_authenticated, get_new_key
from .models import Module
# json
import json
from django.core import serializers
# errors
from django.db.utils import IntegrityError
from django.http import Http404

#to be anihilated
from .models import Task
from .form import ModuleForm
from main.models import UserNote
from groups.models import Group


def CreateView(request):
    if not is_user_authenticated(request):
        return redirect("/accounts/register/tasks_create")

    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        return render(request, 'module_create.html', context)

    # scrap data
    name        = request.POST['name']
    description = request.POST['description']
    author      = request.user

    # validation
    if len(Module.objects.filter(name=name, author=author)):
        return redirect('/tasks/create/')
        
    # create
    try:
        new_module = Module.objects.create(
            name        = name,
            author      = author,
            description = description,
            id          = get_new_key()
        )
    except IntegrityError: pass
    
    # save
    new_module.save()
    # proceed
    return redirect(f'/tasks/{new_module.id}/')
# CreateModuleView - end


def ShowView(request, id):

    context = get_base_context(request)

    # does id exist
    try: context['module'] = Module.objects.get(id=id)
    except Module.DoesNotExist: raise Http404

    # render page
    if request.method != 'POST':
        return render(request, 'module_show.html', context) 
    
    # what request
    if request.POST["btn_edit"]:
        return redirect(f'/tasks/{id}/edit')
    if request.POST["btn_pass"]:
        return redirect(f'/tasks/{id}/pass')

    # what?
    return redirect(f'/tasks/{id}/')    
#ShowModuleView-end

def EditView(request):pass
def PassView(request):pass

def FindView(request):
    context = get_base_context(request, 'Найти модуль')
    context['to_find'] = request.POST.get('to_search', "")
    if request.method == 'POST':
        context['to_show'] = sorted(Module.objects.filter(is_active=True,is_public=True, name__startswith=request.POST['to_search']), key=lambda m: m.creation_date, reverse=True)[:10]
    else:
        context['to_show'] = sorted(Module.objects.filter(is_active=True,is_public=True), key=lambda m: m.creation_date, reverse=True)[:10]
    return render(request, 'module_find.html', context) 