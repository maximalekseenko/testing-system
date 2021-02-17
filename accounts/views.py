from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from static.py.view import get_base_context


def LoginView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #login
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #login-end
            return redirect('/')
    else:
        form = UserCreationForm()


def RegisterView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #login
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #login-end
            return redirect('/')
    else:
        form = UserCreationForm()

    args = {'form': form, 'button': 'register'}
    return render(request, 'registration/register.html', args)


def AccoutView(request):
    return render(request, 'account.html')
