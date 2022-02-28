from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from static.py.view import get_base_context
#to be anihilated
from .forms import AccountForm

def LoginView(request):
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        return render(request, 'registration/login.html', context)

    # scrap data
    username    = request.POST['username']
    password    = request.POST['password']
    user        = authenticate(request, username=username, password=password)

    # validation
    if user is None:
        return redirect(f'/accounts/login/')

    # login
    login(request, user)
 
    # return to previous page
    return redirect(request.COOKIES['before_sign_page'])
# LoginView - end

        
def RegisterView(request):
    # render page
    if request.method != 'POST':
        context = get_base_context(request)
        context['form'] = UserCreationForm()
        response=render(request, 'registration/register.html', context)
        return response

    # scrap data
    form = UserCreationForm(request.POST)
    
    # validation
    if not form.is_valid():
        return redirect(f'/accounts/register/')

    # save
    form.save()

    #login
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=password)
    login(request, user)

    # return to previous page
    return redirect(request.COOKIES['before_sign_page'])
# RegisterView - end


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
