from urllib.parse import urljoin

import weasyprint
from celery import shared_task

from django.template.loader import render_to_string
from django.templatetags.static import static
from django.core.mail import EmailMultiAlternatives

from orders.models import Order



@shared_task
def payment_completed(order_id, base_url):
    '''
    A task to send the email with an atatchment of invoice to the user after successfull payment.
    
    '''

    # retrive the order obj and render the template
    order = Order.objects.get(id=order_id)
    html  = render_to_string('templates/pdf.html', {'order': order})

    # convert the html to pdf bytes
    pdf_bytes = weasyprint.HTML(string=html).write_pdf()

    # compose email
    logo_url = urljoin(base_url, static('templates/emails/logo.png'))
    context = {'order': order,
               'logo_url': logo_url
               }
    subject = 'Payment received - Altas gearbox.'
    txt_body = render_to_string('templates/emails/order_paid.txt', context)
    html_body = render_to_string('templates/emails/order_paid.html', context)
    email = EmailMultiAlternatives(subject, txt_body, to=[order.address.email])
    email.attach_alternative(html_body, 'text/html')

    # Attach the pdf bytes and send the mail
    email.attach(f'order_{order.id}.pdf', pdf_bytes, 'application/pdf')
    email.send()

