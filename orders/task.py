from django.core.mail import send_mail

from .models import Order

from celery import shared_task



@shared_task
def order_created(order_id):
    """
    Task to send an email to the user when an order successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name}, /n/n' 
        f'You have successfully placed an order.'
        f'Your order ID is {order.id}'
    )
    mail_sent = send_mail(subject, message, 'admin@gmail.com', [order.email])

    return mail_sent