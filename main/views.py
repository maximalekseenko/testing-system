from django.shortcuts import render

def HomeView(request):
    is_teacher = True
    args={"is_teacher": is_teacher}
    return render(request, 'home.html', args)

def HeresyoneView(request):
    return  render(request, 'heresypage1.html')