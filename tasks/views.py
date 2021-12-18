from django.shortcuts import render, redirect
from static.py.view import get_base_context, is_user_authenticated, get_new_key
from .models import Module
import json
# errors
from django.db.utils import IntegrityError
from django.http import Http404


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
# CreateView - end


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
# ShowView - end


def EditView(request, id):
    # does id exist
    try: cur_module = Module.objects.get(id=id)
    except Module.DoesNotExist: raise Http404

    # is user author 
    if cur_module.author != request.user: raise Http404

    # render page
    if request.method != 'POST':
        context = get_base_context(request, keep_cookies=[f"temp_edit_tasks_data_{cur_module.id}", f"temp_edit_module_{cur_module.id}"])
        # imoprt module from cookies
        if f'temp_edit_module_{cur_module.id}' not in request.session: context['module'] = cur_module
        else: context['module'] = request.session[f'temp_edit_module_{cur_module.id}']
        # imoprt tasks from cookies
        if f'temp_edit_tasks_data_{cur_module.id}' not in request.session: context['tasks_data'] = cur_module.tasks_data
        else: context['tasks_data'] = request.session[f'temp_edit_tasks_data_{cur_module.id}']
        # proceed
        return render(request, 'module_edit.html', context) 
    
    # cancel
    if "cancel_btn" in request.POST:
        return redirect(f'/tasks/{id}/')


    # delete module
    if 'btn_del' in request.POST:
        cur_module.delete()
        return redirect(f'/')

    # scrap data
    name            = request.POST['name']
    description     = request.POST['description']
    is_tasks_rnd    = 'is_tasks_rnd' in request.POST

    # save module
    if 'btn_save' in request.POST:
        cur_module.name = name
        cur_module.description = description
        cur_module.is_tasks_rnd = is_tasks_rnd
        if f'temp_edit_tasks_data_{cur_module.id}' in request.session:
            cur_module.tasks_data = request.session[f'temp_edit_tasks_data_{cur_module.id}']
        cur_module.save()
        return redirect(f'/tasks/{id}/') 

    # edit task
    task_num=list(filter(lambda d:d.startswith("btn_task"), request.POST))
    if task_num:
        # export module to cookies
        request.session[f'temp_edit_module_{cur_module.id}']={'name':name,'description':description,'is_tasks_rnd':is_tasks_rnd}
        # export task to cookies
        if not f'temp_edit_tasks_data_{cur_module.id}' in request.session:
            request.session[f'temp_edit_tasks_data_{cur_module.id}'] = cur_module.tasks_data
        # proceed
        return redirect(f'/tasks/{id}/edit/{task_num[0][9:]}')
# EditView - end


def EditTaskView(request, id, tn):
    # does id exist
    try: cur_module = Module.objects.get(id=id)
    except Module.DoesNotExist: raise Http404

    # is user author 
    if cur_module.author != request.user: raise Http404

    # render page
    if request.method != 'POST':
        context = get_base_context(request, keep_cookies=[f"temp_edit_tasks_data_{cur_module.id}", f"temp_edit_module_{cur_module.id}"])
        # tasks imoprt
        if f'temp_edit_tasks_data_{cur_module.id}' not in request.session: tasks_data = cur_module.tasks_data
        else: tasks_data = request.session[f'temp_edit_tasks_data_{cur_module.id}']
        # get task
        if tn < len(tasks_data): context['task_data'] = tasks_data[tn]
        else: context['task_data'] = {"name":"","condition":"","ans_type":"one_answer","ans_cor":[""],"ans_opt":[""],"ans_rnd":0}
        # proceed
        return render(request, 'module_edit_task.html', context) 

    # cancel
    if "cancel_btn" in request.POST:
        return redirect(f'/tasks/{id}/edit/')

    # scrap data
    name        = request.POST['name']
    condition   = request.POST['condition']
    ans_type    = request.POST['ans_type']
    ans_cor     = dict(request.POST)['ans_cor'] if 'ans_cor' in request.POST  else []
    ans_opt     = dict(request.POST)['ans_opt'] if 'ans_opt' in request.POST  else []
    ans_rnd     = int('ans_rnd' in request.POST)

    # add task to cookies if new
    if tn == len(request.session[f'temp_edit_tasks_data_{cur_module.id}']):
        request.session[f'temp_edit_tasks_data_{cur_module.id}'].append({"name":"","condition":"","ans_type":"one_answer","ans_cor":[""],"ans_opt":[""],"ans_rnd":0})

    # save task to cookies
    task_data = request.session[f'temp_edit_tasks_data_{cur_module.id}']
    task_data[tn] = {"name":name,"condition":condition,"ans_type":ans_type,"ans_cor":ans_cor,"ans_opt":ans_opt,"ans_rnd":ans_rnd}
    request.session[f'temp_edit_tasks_data_{cur_module.id}'] = task_data
    
    # proceed
    return redirect(f'/tasks/{id}/edit')    
# EditTaskView - end


def DelTaskView(request,id, tn):
    if f'temp_edit_tasks_data_{id}' in request.session:
        if tn < len(request.session[f'temp_edit_tasks_data_{id}']):
            del request.session[f'temp_edit_tasks_data_{id}'][tn]
            request.session.modified = True
    return redirect(f'/tasks/{id}/edit/')
# DelTaskView - end


def PassView(request):pass


def FindView(request):
    context = get_base_context(request)
    context['to_find'] = request.POST.get('to_search', "")
    if request.method == 'POST':
        context['to_show'] = sorted(Module.objects.filter(is_active=True,is_public=True, name__startswith=request.POST['to_search']), key=lambda m: m.creation_date, reverse=True)[:10]
    else:
        context['to_show'] = sorted(Module.objects.filter(is_active=True,is_public=True), key=lambda m: m.creation_date, reverse=True)[:10]
    return render(request, 'module_find.html', context) 