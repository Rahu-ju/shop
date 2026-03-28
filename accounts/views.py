from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .forms import UserResgistrationForm, UserEditForm, ProfileEditForm
from .models import Profile



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

            # create profile objects of the new user
            Profile.objects.create(user=new_user)

            return render(request, 'accounts/registration_done.html', {'new_user': new_user} )
        else:
            return render(request, 'accounts/registration.html', {'form': form})

    else:
        form = UserResgistrationForm()
        return render(request, 'accounts/registration.html', {'form': form})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # send message to the user.
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'accounts/edit.html', {'user_form': user_form, 'profile_form': profile_form})