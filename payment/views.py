from decimal import Decimal
import stripe

from django.shortcuts import render, get_object_or_404,redirect
from django.conf import settings
from django.urls import reverse

from orders.models import Order



stripe.api_key = settings.STRIPE_SECRET_KEY
# stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):

    #get the order id from session, and retrieve the order object from database
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':

        # define and generate sucess and cancel uri 
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        #Generate session data for stripe checkout and create stripe checkout session
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        #generate line_item for session_data
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data': {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name
                        },
                    },
                    'quantity': item.quantity,
                }
            )

        session = stripe.checkout.Session.create(**session_data)

        return redirect(session.url, 303)

    return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')

