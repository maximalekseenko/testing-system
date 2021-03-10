from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from static.py.view import get_base_context
from .forms import AccountForm


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
    context = get_base_context(request, "Регистрация")
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
    context['form'] = form
    return render(request, 'registration/register.html', context)



def AccoutView(request):
    context = get_base_context(request, "")
    if request.method == 'POST':
        form = AccountForm(request.POST)
        request.user.userprofile.status = form.data['status']
        request.user.userprofile.bio    = form.data['bio']
        request.user.userprofile.metall = form.data['metall']
        request.user.userprofile.save()
        return redirect(f'/')
    #if POST-end
    context['form'] = AccountForm(
        initial={
            'username'  : request.user.username,
            'status'    : request.user.userprofile.status,
            'bio'       : request.user.userprofile.bio,
            'metall'    : request.user.userprofile.metall,
    })
    return render(request, 'account.html', context)
