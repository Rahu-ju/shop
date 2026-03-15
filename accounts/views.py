from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from .forms import LoginForm, UserResgistrationForm



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



def register(request):
    if request.method == 'POST':

        # take form data and check its valid or not
        form = UserResgistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # before save, feed the password to the model form
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            return render(request, 'accounts/registration_done.html', {'new_user': new_user} )
    else:
        form = UserResgistrationForm()
        return render(request, 'accounts/registration.html', {'form': form})