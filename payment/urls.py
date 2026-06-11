from django.urls import path

from . import views, webhooks



app_name='payment'
urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
    # For paying with bkash
    path('bkash/pay/', views.bkash_payment_initiate, name='bkash_payment_initiate'),
    path('bkash/callback/', views.bkash_payment_callback, name='bkash_payment_callback'),
]
