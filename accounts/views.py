from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import LoginForm



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    HttpResponse('Authenticated successfully')
                else:
                    HttpResponse('Account is not active')
            else:
                HttpResponse('User information is wrong')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form })



def dashboard(request):
    dashboard = None
    return render(request, 'accounts/dashboard.html', {'dashboard': dashboard} )