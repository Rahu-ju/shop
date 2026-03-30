import uuid

from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(null=True, blank=True)
    token_created_at = models.DateTimeField(null=True, blank=True)


    def is_token_expired(self):
        ''' The expire time is 5 minutes from the token creation time.'''

        expiry_time = self.token_created_at + timedelta(minutes=5)
        return timezone.now() > expiry_time


    def generate_new_token(self):
        self.verification_token = uuid.uuid4()
        self.token_created_at = timezone.now()
        self.save()
        
    def __str__(self):
        return f'Profile of {self.user.username}'