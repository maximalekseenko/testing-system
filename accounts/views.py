from django.shortcuts import render, redirect
from accounts.forms import RegisrationForm
from django.contrib.auth import login, authenticate

def RegisterView(request):
    if request.method == 'POST':
        form = RegisrationForm(request.POST)
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
        form = RegisrationForm()

    args = {'form': form, 'button': 'register'}
    return render(request, 'registration/register.html', args)
