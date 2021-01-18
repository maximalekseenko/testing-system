from django.shortcuts import render

def HomeView(request):
    return render(request, 'home.html')

def HeresyoneView(request):
    return  render(request, 'heresypage1.html')