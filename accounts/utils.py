from django.core.mail import send_mail
from django.urls import reverse



def send_verification_email(request, user):
    ''' It will send a mail to the user with a verification link.'''

    token = user.profile.verification_token
    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'token': token})
    )

    send_mail(
        subject='Verify Your email. You have 5 minutes only.',
        message=f'Click the link to verify your email: \n {verification_link} \n\n This link will expire in 5 minutes.',
        from_email='altas.admin@gmail.com',
        recipient_list=[user.email,]
    )
