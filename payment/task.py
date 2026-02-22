import weasyprint
from celery import shared_task
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage

from orders.models import Order



@shared_task
def payment_completed(order_id):
    '''
    A task to send the email with an atatchment of invoice to the user after successfull payment.
    
    '''

    # retrive the order obj and render the template
    order = Order.objects.get(id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})

    # get css file and compose pdf bytes
    css_file = finders.find('shop/css/pdf.css')
    pdf_bytes = weasyprint.HTML(string=html).write_pdf(stylesheets=[weasyprint.CSS(css_file)])

    # compose email
    subject = f'My shop - invoice no {order.id}'
    message = 'Please see the attachment,  the details of your purchase'
    email = EmailMessage(subject, message, 'admin.ju@gmail.com', [order.email])

    # Attach the pdf bytes and send the mail
    email.attach(f'order_{order.id}.pdf', pdf_bytes, 'application/pdf')
    email.send()

