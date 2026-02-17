import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order



@csrf_exempt
def stripe_webhook(request):

    # Taking the request body and stripe signature header from the request
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    
    # Now create stripe event by feeding above variables
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    #Checking event type
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                # Get the order using client refenence id 
                order = Order.objects.get(id=session.client_reference_id)

            except Order.DoesNotExist:
                return HttpResponse(status=404)
            
            # Marking order paid field to true and save it.
            order.paid = True
            print(session.payment_intent)
            order.stripe_id = session.payment_intent
            order.save()
            

    return HttpResponse(status=200)
    