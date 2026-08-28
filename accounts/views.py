import uuid

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone


from .forms import SignUpForm, UserEditForm, ProfileEditForm
from .models import Profile
from .utils import send_verification_email
from .models import CustomUser



def dashboard(request):
    dashboard = None
    return render(request, 'templates/dashboard.html', {'dashboard': dashboard} )



def signup_view(request):
    if request.method == 'POST':

        # Feed the post  data to the user
        form = SignUpForm(request.POST)

        if form.is_valid():

            # Create the new user and by default is_active False
            new_user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )

            # create profile of the new user
            Profile.objects.create(
                user=new_user, 
                verification_token=uuid.uuid4(), 
                token_created_at=timezone.now()
            )

            # send a mail for verification link
            send_verification_email(request, new_user)

            # Send message
            messages.info(request, 'Verification link has been sent')

            return render(request, 'templates/email_verification.html', {'new_user': new_user, 'send_link': True} )
        else:
            return render(request, 'templates/signup.html', {'form': form})

    else:
        return render(request, 'templates/signup.html')



def signin_view(request):
    if request.method == "POST":

        # getting the user info from post data
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        # log the user in
        if user is not None:
            login(request, user)
            return redirect('shop:home')
        
        return render(request, 'templates/login.html', {'error': "invalid credentials"})
    return render(request, 'templates/login.html')



def signout_view(request):

    # let the user to logout
    logout(request)

    return redirect('shop:home')



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
        return render(request, 'templates/email_verification.html', {'token': token, 'token_expired': True,})
    
    # activate the account
    profile.email_verified = True
    profile.user.is_active = True
    profile.user.save()
    profile.save()
    
    messages.info(request, 'Account verified.')
    return render(request, 'templates/email_verification.html', {'verified': True})



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
    return render(request, 'templates/email_verification.html', {'send_link': True})    