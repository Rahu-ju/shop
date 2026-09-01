from django.core.mail import send_mail
from django.urls import reverse

from celery import shared_task



@shared_task
def send_verification_email(verification_link, email):
    ''' It will send a mail to the user with a verification link.'''

    send_mail(
        subject='Verify Your email. You have 5 minutes only.',
        message=f'Click the link to verify your email: \n {verification_link} \n\n This link will expire in 5 minutes.',
        from_email='altas.admin@gmail.com',
        recipient_list=[email,]
    )
