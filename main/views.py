from django.shortcuts import render
from main.models import test1

def HomeView(request):
    is_teacher = True
    args={"is_teacher": is_teacher}
    return render(request, 'home.html', args)

def HeresyoneView(request):
    test = test1.objects.first()

    args={
        "test" : test,
        "TEST" : "TEST",
    }

    return render(request, 'heresypage1.html', args)