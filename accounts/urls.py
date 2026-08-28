from django.urls import include, path

from . import views



# Define app name
app_name = 'account'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('register/', views.signup_view, name='register'),
    path('signin/', views.signin_view, name='custom_login'),
    path('signout/', views.signout_view, name='custom_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('resend-email/<uuid:token>/', views.resend_email_verification, name='resend_email'),
]
