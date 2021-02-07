from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Task
from .form import AddTaskForm
from django.http import Http404

def get_base_context(request, pagename):
    return {
        'pagename': pagename,
        'user': request.user,
    }


def HomeView(request):
    context = get_base_context(request, "Главная")
    return render(request, 'home.html', context)


def HeresyoneView(request):
    context = get_base_context(request, "ы")
    return render(request, 'heresypage1.html', context)


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
            id = new_task.id
            # messages.add_message(request, messages.SUCCESS, "Задание успешно добавлено")
            return redirect(f'/showtask/{id}/')
        else:
            # messages.add_message(request, messages.ERROR, "Некорректные данные в форме")
            return redirect('taskcreation/')
    else:
        context['addform'] = AddTaskForm(
            initial={
                'user': request.user,
            }
        )
    return render(request, 'createtask.html', context)


def EditTaskView(request):
    if request.user.userprofile.user_type != "teacher":
        return redirect("/accounts/")
    if request.method == "POST":
        task = Task(name=request.POST.get("name"), content=request.POST.get("content"))
        task.save()
        return redirect("/")
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
