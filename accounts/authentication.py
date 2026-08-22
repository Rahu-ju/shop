'''
Django authenticate the user using their username and then password,
But this authentication backend alllow user to authenticate with 
their email too and then password.

So essencially user can be authenticate with their username or email and password
'''

from django.contrib.auth import get_user_model


User = get_user_model()


class EmailAuthBackend:
    ''' 
    Authenticate using email.
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
        # checking password for super user or staff
        if user.is_active and user.is_superuser:
            if password and user.check_password(password):
                return user
            return None

        return user
        

        
        

    # def get_user(self, user_id):
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None

