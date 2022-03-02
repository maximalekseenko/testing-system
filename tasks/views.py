from django.shortcuts import render, redirect
from static.py.view import get_base_context, get_new_key, get_element_by_starts_with, get_elements_by_starts_with
from static.py.decorators import check_auntification, check_object_exist, check_author
from .models import Module,Task,Answer
from random import shuffle
from groups.models import Group, UserMark
from django.utils import timezone
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
        context = get_base_context(request)
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
        context = get_base_context(request)
        context['task'] = cur_task
        ## render
        return render(request, 'module_edit_task.html', context) 

    # save
    cur_task.name = request.POST['name']
    cur_task.condition = request.POST['condition']
    cur_task.type = request.POST['task_type']
    cur_task.is_answer_rnd = 'is_random' in request.POST
    ## get answers count
    answers_count = len(list(filter(lambda e:e.startswith('answer_value_'), request.POST)))
    ## add answers if needed
    for i in range(answers_count-len(cur_task.answers.all())):
        new_answer = Answer()
        new_answer.save()
        cur_task.answers.add(new_answer)
    ## remove extra
    for i in range(len(cur_task.answers.all())-answers_count):
        cur_task.answers.all()[len(cur_task.answers.all())-1].delete()
    ## fill answers with request data
    for i in range(answers_count):
        cur_answer = cur_task.answers.all()[i]
        ### set is_correct
        cur_answer.is_correct = False
        if cur_task.type=="one" and f'correct_answer_' in request.POST: 
            cur_answer.is_correct = int(request.POST[f'correct_answer_']) == i
        if cur_task.type=="multy": 
            cur_answer.is_correct = f'correct_answer_{i}' in request.POST
        if cur_task.type=="text":
            cur_answer.is_correct=True
        ### set value
        cur_answer.value = request.POST[f'answer_value_{i}']
        ### save
        cur_answer.save()
    ## save
    cur_task.save()

    # proceed
    return redirect(f'/tasks/edit/?id={cur_module.id}')
# EditTaskView - end



@check_object_exist(Module)
def PassView(request, cur_module):
    # set sessions
    if f'module_{cur_module.id}_pass' not in request.session:
        ## get tasks order
        task_order = list(range(len(cur_module.tasks.all())))
        if cur_module.is_tasks_rnd: shuffle(task_order)
        ## set sessions
        request.session[f'module_{cur_module.id}_pass'] = []
        for task_num in task_order: request.session[f'module_{cur_module.id}_pass'].append([task_num, []])
        request.session[f'module_{cur_module.id}_pass_i'] = 0
    

    # checks
    ## cancel check
    if request.session[f'module_{cur_module.id}_pass_i'] < 0:
        del request.session[f'module_{cur_module.id}_pass']
        del request.session[f'module_{cur_module.id}_pass_i']
        if f'module_{cur_module.id}_group' in request.session:
            redirect_to_group_id = request.session[f'module_{cur_module.id}_group']
            del request.session[f'module_{cur_module.id}_group']
            return redirect(f'/groups/?id={redirect_to_group_id}')
        return redirect(f'/tasks/?id={cur_module.id}')
    ## finish check
    elif request.session[f'module_{cur_module.id}_pass_i'] > len(request.session[f'module_{cur_module.id}_pass']) -1:
        return redirect(f'/tasks/result/?id={cur_module.id}')

    
    # get current task
    cur_task = cur_module.tasks.all()[request.session[f'module_{cur_module.id}_pass'][request.session[f'module_{cur_module.id}_pass_i']][0]]
    
    
    # render page
    if request.method != 'POST':
        ## get context
        context = get_base_context(request)
        context['is_last']  = request.session[f'module_{cur_module.id}_pass_i'] >= len(request.session[f'module_{cur_module.id}_pass']) -1
        context['is_first'] = request.session[f'module_{cur_module.id}_pass_i'] <= 0
        context['task'] = cur_task
        context['given_answers'] = request.session[f'module_{cur_module.id}_pass'][request.session[f'module_{cur_module.id}_pass_i']][1]
        ## render
        return render(request, 'module_pass.html', context) 

    
    # get answers
    if cur_task.type=='one':    new_answers = [request.POST.get('selected_answer')]
    elif cur_task.type=='multy':new_answers = sorted(list(map(lambda i:request.POST[f'selected_answer_{i}'], get_elements_by_starts_with('selected_answer_', request))))
    elif cur_task.type=='text': new_answers = [request.POST.get('selected_answer')]


    # set answers
    request.session[f'module_{cur_module.id}_pass'][request.session[f'module_{cur_module.id}_pass_i']][1] = new_answers


    # what request
    ## previous
    if 'btn_previous' in request.POST:
        request.session[f'module_{cur_module.id}_pass_i'] -=1
    ## next
    if 'btn_next' in request.POST:
        request.session[f'module_{cur_module.id}_pass_i'] +=1
    

    # reload
    return redirect(request.get_raw_uri())



@check_object_exist(Module)
def ResultView(request, cur_module):
    if f'module_{cur_module.id}_pass' not in request.session: raise Http404


    # render page
    if request.method != 'POST':
        ## get context
        context = get_base_context(request)
        context['module'] = cur_module
        context['given_answers'] = request.session[f'module_{cur_module.id}_pass']
        ## render
        return render(request, 'module_result.html', context)
        

    # save result to group
    if f'module_{cur_module.id}_group' in request.session:
        cur_module_data = Group.objects.get(id=request.session[f'module_{cur_module.id}_group']).moduls_data.get(module=cur_module)
        ##
        given_answers = list(map(lambda x:x[1], sorted(request.session[f'module_{cur_module.id}_pass'])))
        ## count correct answers given
        correct_answers_num = 0
        for i in range(len(cur_module.tasks.all())):
            _cur_task = cur_module.tasks.all()[i]
            _cur_task_correct_answers = sorted(map(lambda x: x.value,_cur_task.answers.filter(is_correct=True)))
            if _cur_task.type == 'one': 
                if given_answers[i] != _cur_task_correct_answers: continue
            if _cur_task.type == 'multy': 
                if given_answers[i] != _cur_task_correct_answers: continue
            if _cur_task.type == 'text': 
                if given_answers[i][0] not in _cur_task_correct_answers: continue
            correct_answers_num += 1
        ## create mark object
        new_user_mark = UserMark(
            user=request.user,
            mark=0 if correct_answers_num == 0 else round(correct_answers_num / len(cur_module.tasks.all()) * 100),
            is_before_deadline = timezone.now() <= cur_module_data.deadline)
        new_user_mark.save()
        cur_module_data.user_marks.add(new_user_mark)


    del request.session[f'module_{cur_module.id}_pass']
    del request.session[f'module_{cur_module.id}_pass_i']
    if f'module_{cur_module.id}_group' in request.session:
        redirect_to_group_id = request.session[f'module_{cur_module.id}_group']
        del request.session[f'module_{cur_module.id}_group']
        return redirect(f'/groups/?id={redirect_to_group_id}')

    
    # return
    return redirect(f'/tasks/?id={cur_module.id}')



    