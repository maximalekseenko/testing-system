from asyncio import tasks
from django.shortcuts import render, redirect
from static.py.view import get_base_context, get_new_key, get_element_by_starts_with, get_elements_by_starts_with
from static.py.decorators import check_auntification, check_object_exist, check_author
from .models import Module,Task,Answer
# errors
from django.db.utils import IntegrityError
from django.http import Http404



@check_auntification
def CreateView(request):
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        return render(request, 'module_create.html', context)


    # create
    while True:
        try:
            new_module = Module.objects.create(
                name        = request.POST['name'],
                description = request.POST['description'],
                author      = request.user,
                id          = get_new_key())
            break
        except IntegrityError: continue
    

    # save
    new_module.save()

    
    # proceed
    return redirect(f'/tasks/?id={new_module.id}')
# CreateView - end



@check_object_exist(Module)
def ShowView(request, cur_module):
    # render page
    if request.method != 'POST':
        ## get context
        context = get_base_context(request)
        context['module'] = cur_module
        ## render
        return render(request, 'module_show.html', context) 
    

    # what request
    ## edit
    if "btn_edit" in request.POST:
        return redirect(f'/tasks/edit/?id={cur_module.id}')
    ## pass
    if "btn_pass" in request.POST:
        return redirect(f'/tasks/pass/?id={cur_module.id}')


    # reload
    return redirect(request.get_raw_uri())
# ShowView - end



@check_object_exist(Module)
@check_author
def EditView(request, cur_module):
    # render page
    if request.method != 'POST':
        ## get context
        context = get_base_context(request, keep_cookies=[f"temp_edit_tasks_data_{cur_module.id}", f"temp_edit_module_{cur_module.id}"])
        context['module'] = cur_module
        ## render
        return render(request, 'module_edit.html', context) 
    

    # what request
    ## delete
    if 'btn_del' in request.POST:
        cur_module.delete()
        return redirect(f'/')
    ## save
    if 'btn_save' in request.POST:
        cur_module.name = request.POST['name']
        cur_module.description = request.POST['description']
        cur_module.is_tasks_rnd = 'is_tasks_rnd' in request.POST
        if f'temp_edit_tasks_data_{cur_module.id}' in request.session:
            cur_module.tasks_data = request.session[f'temp_edit_tasks_data_{cur_module.id}']
        cur_module.save()
        return redirect(f'/tasks/?id={cur_module.id}') 
    ## task create
    if 'btn_task_create' in request.POST:
        new_task = Task()
        new_task.save()
        cur_module.tasks.add(new_task)
        return redirect(f'/tasks/edit/task?id={cur_module.id}&t={len(cur_module.tasks.all())-1}') 
    ## task delete
    task_num = get_element_by_starts_with("btn_task_delete_",request)
    if task_num:
        cur_module.tasks.all()[int(task_num)].delete()
    ## task edit
    task_num = get_element_by_starts_with("btn_task_edit_",request)
    if task_num:
        return redirect(f'/tasks/edit/task?id={cur_module.id}&t={task_num}')


    # reload
    return redirect(request.get_raw_uri())
# EditView - end



@check_object_exist(Module)
@check_author
def EditTaskView(request, cur_module):
    cur_task = cur_module.tasks.all()[int(request.GET['t'])]

    # render page
    if request.method != 'POST':
        ## get context
        context = get_base_context(request, keep_cookies=[f"temp_edit_tasks_data_{cur_module.id}", f"temp_edit_module_{cur_module.id}"])
        context['task'] = cur_task
        ## render
        return render(request, 'module_edit_task.html', context) 


    # correct_answer
    # answer_value
    # what request
    ## 
    if "btn_save" in request.POST:
        cur_task.name = request.POST['name']
        cur_task.condition = request.POST['condition']
        answers_count = len(list(filter(lambda e:e.startswith('answer_value_'), request.POST)))
        cur_task.type = request.POST['task_type']
        cur_task.is_answer_rnd = 'is_random' in request.POST
        ### add answers if needed
        for i in range(answers_count-len(cur_task.answers.all())):
            new_answer = Answer()
            new_answer.save()
            cur_task.answers.add(new_answer)
        ### remove extra
        for i in range(len(cur_task.answers.all())-answers_count):
            cur_task.answers.all()[len(cur_task.answers.all())-1].delete()
        ### fill answers with request data
        for i in range(answers_count):
            cur_answer = cur_task.answers.all()[i]
            cur_answer.is_correct = f'correct_answer_{i}' in request.POST
            cur_answer.value = request.POST[f'answer_value_{i}']
            cur_answer.save()
        ### save
        cur_task.save()
        return redirect(f'/tasks/edit/?id={cur_module.id}')
    ## 
    if "btn_answer_add" in request.POST:
        pass
    ## 
    if "btn_answer_rem" in request.POST:
        pass

    # reload
    return redirect(request.get_raw_uri())  
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