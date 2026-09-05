import uuid

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

from .forms import SignUpForm, SignInForm, UserEditForm, ProfileEditForm
from .models import Profile
from .task import send_verification_email
from .models import CustomUser



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
            user_profile = Profile.objects.create(
                user=new_user, 
                verification_token=uuid.uuid4(), 
                token_created_at=timezone.now()
            )

            # send a mail with a verification link via celery
            token = user_profile.verification_token
            email = new_user.email
            verification_link = request.build_absolute_uri(
                reverse('account:verify_email', kwargs={'token': token})
                )
            send_verification_email.delay(verification_link, email)

            context = {
                'username': new_user.username,
                'verified': False,
                'headline': 'Account created successfully',
                'message': 'We have sent a verification link to your mail. Please check your mail and verify your account.'
            }
            return render(request, 'templates/email_verification.html', context)
        else:
            return render(request, 'templates/signup.html', {'form': form})

    else:
        return render(request, 'templates/signup.html')



def signin_view(request):

    if request.method == "POST":

        # Feed the post data to the form
        form = SignInForm(request.POST)
        if form.is_valid():

            # Take the user object from the form, 
            # Addded intentionally to avoid DB query again.
            user = form.cleaned_data['user']

            # log the user in if active
            if user.is_active:
                login(request, user)
                return redirect('shop:home')

            # depends on the token expiration, show the message to the user.
            if user.profile.is_token_expired():
                context = { 'verified': False, 
                            'token': user.profile.verification_token,
                            'username': user.username,
                            'headline': 'Account not verified yet',
                            'message': 'The verification time has expired. Please request a new one.'
                            }
                
                return render(request, 'templates/email_verification.html', context)
            else:
                context = { 'verified': False,
                            'username': user.username,
                            'headline': 'Email not verified yet',
                            'message': 'You are not verified yet, Check your mail, we already sent the verification link.'
                            }
                return render(request, 'templates/email_verification.html', context)   
             
        return render(request, 'templates/login.html', {'form': form,})
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

        
        context = { 'verified': False, 
                   'token': token, 
                   'username': profile.user.username,
                    'headline': 'Verification link expired',
                    'message': 'The verification link has expired. Please request a new one.'
                   }
        return render(request, 'templates/email_verification.html', context)
    
    # activate the account
    profile.email_verified = True
    profile.user.is_active = True
    profile.user.save()
    profile.save()
    
    messages.info(request, 'Account verified.')
    return render(request, 'templates/email_verification.html', {'verified': True, 'email': profile.user.email,})



def resend_email_verification(request, token):
    '''
    It will resend the verification link via mail.
    '''
    # retrive profile and user
    profile = get_object_or_404(Profile, verification_token=token)
    username = profile.user.username
    email = profile.user.email

    # generate new token
    profile.generate_new_token()

    # send the mail asynchronoulsy via celery
    verification_link = request.build_absolute_uri(
        reverse('account:verify_email', kwargs={'token': profile.verification_token})
    )
    send_verification_email.delay(verification_link, email)

    messages.info(request, 'verification link sent, once again.')
    context = { 'send_link': True, 
                'username': username,
                'headline': 'Verification link sent',
                'message': 'We have sent the verification link to your mail, again. Please check your mail.'
               }
    return render(request, 'templates/email_verification.html', context)    