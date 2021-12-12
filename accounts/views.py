from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from static.py.view import get_base_context
#to be anihilated
from .forms import AccountForm

def LoginView(request, red=""):
    context = get_base_context(request)
    context['redirect'] = red

    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'/{"/".join(red.split("_"))}')
        else:
            context['login_error'] = True

    return render(request, 'registration/login.html', context)

        
def RegisterView(request, red=""):
    context = get_base_context(request)
    context['redirect'] = red

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
            return redirect(f'/{"/".join(red.split("_"))}')
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
    })
    return render(request, 'account.html', context)
