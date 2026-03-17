'''
Django authenticate the user using their username and then password,
But this authentication backend alllow user to authenticate with 
their email too and then password.

So essencially user can be authenticate with their username or email and password
'''

from django.contrib.auth.models import User


class EmailAuthBackend:
    ''' 
    Authenticate using email.
    '''

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except(User.DoesNotExist or User.MultipleObjectsReturned):
            return None
        

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

