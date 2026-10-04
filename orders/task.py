from urllib.parse import urljoin

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.templatetags.static import static

from .models import Order

from celery import shared_task



@shared_task
def order_created(order_id, base_url):
    """
    Task to send an email to the user when an order successfully created.
    """
    order = Order.objects.get(id=order_id)
    logo_url = urljoin(base_url, static('templates/emails/logo.png'))
    context = {'order': order,
               'logo_url': logo_url,
               }
    subject = "Your Order placed — Atlas-gearbox"
    text_body = render_to_string("templates/emails/verify-email.txt", context)
    html_body = render_to_string("templates/emails/order_placed.html", context)
    

    msg = EmailMultiAlternatives(subject, text_body, to=[order.address.email])
    msg.attach_alternative(html_body, "text/html")
    msg.send()