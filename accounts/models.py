import uuid

from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
from django.utils import timezone



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):

        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password=None, **extra_fields):

        if not email:
            raise ValueError("The Email field must be set for superuser")
        if not password:
            raise ValueError("The password field must be set for superusers")

        # Force essential fields for superuser
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        extra_fields['is_active'] = True

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user





class CustomUser(AbstractBaseUser, PermissionsMixin):
    ''' 
    This is a custom user model that extends the default Django user model.
    '''
    username = models.CharField(max_length=30, default='')
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(null=True, blank=True)
    token_created_at = models.DateTimeField(null=True, blank=True)


    def is_token_expired(self):
        ''' The expire time is 5 minutes from the token creation time.'''

        actual_expiry_time = self.token_created_at + timedelta(minutes=5)
        return timezone.now() > actual_expiry_time


    def generate_new_token(self):
        self.verification_token = uuid.uuid4()
        self.token_created_at = timezone.now()
        self.save()
        
    def __str__(self):
        return f'Profile of {self.user.username}'