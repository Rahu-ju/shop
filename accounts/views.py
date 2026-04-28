import uuid

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils import timezone

from .forms import UserResgistrationForm, CustomAuthForm, UserEditForm, ProfileEditForm
from .models import Profile
from .utils import send_verification_email



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
            new_user.is_active = False
            new_user.save()

            # create profile of the new user
            Profile.objects.create(
                user=new_user, 
                verification_token=uuid.uuid4(), 
                token_created_at=timezone.now()
            )

            # send a mail for verification link
            send_verification_email(request, new_user)

            messages.info(request, 'Verification link has been sent')

            return render(request, 'accounts/registration_done.html', {'new_user': new_user} )
        else:
            return render(request, 'accounts/registration.html', {'form': form})

    else:
        form = UserResgistrationForm()
        return render(request, 'accounts/registration.html', {'form': form})



class SigninView(LoginView):
    form_class = CustomAuthForm




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



def verify_email(request, token):
    '''
    This function will verify the link sent to the mail.
    '''
    # get profile using token
    profile = get_object_or_404(Profile, verification_token=token)

    # check if token expired
    if profile.is_token_expired():

        messages.error(request, 'Verification link expired!!')
        return render(request, 'accounts/email_not_verified.html', {'token': token})
    
    # activate the account
    profile.email_verified = True
    profile.user.is_active = True
    profile.user.save()
    profile.save()
    
    messages.info(request, 'Account verified.')
    return render(request, 'accounts/email_verified.html')



def resend_email_verification(request, token):
    '''
    It will resend the verification link via mail.
    '''
    # retrive profile and user
    profile = get_object_or_404(Profile, verification_token=token)
    user = profile.user

    # generate new token
    profile.generate_new_token()

    # send the mail
    send_verification_email(request, user)

    messages.info(request, 'verification link sent, once again.')
    return render(request, 'accounts/registration_done.html')    