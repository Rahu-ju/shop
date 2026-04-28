from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Profile



class UserResgistrationForm(forms.ModelForm):
    '''
    when form.is_valid() function is called then all the methods of this class will 
    called and raise error accordingly if any.
    '''
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        '''
        This method raise error if two password are not matched.
        '''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Your Passwords don't match")
        return cd['password2']
    
    def clean_email(self):
        '''
        This method raise error if the new user's email already in the databse.
        '''
        email_data = self.cleaned_data['email']
        qs = User.objects.filter(email=email_data)

        if qs.exists():
            raise forms.ValidationError('Email already in use')
        return email_data



class CustomAuthForm(AuthenticationForm):
    def clean(self):
        try:
            return super().clean()
        except ValidationError:
            # check if it's an inactive user with correct password
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()
            
            if user and user.check_password(password) and not user.is_active:
                if user.profile.is_token_expired():
                    raise ValidationError('Your verification lik has been expired, Please Sign up again.!!')
                raise ValidationError('You are not verified yet, Check your mail, we already sent the verification link.')
            raise

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        '''
        This method raise error when an existing user change the mail in the edit profile form
        but it already in the database except his own.
        '''
        email_data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=email_data)

        if qs.exists():
            raise forms.ValidationError('The mail already in use.')
        return email_data



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        

