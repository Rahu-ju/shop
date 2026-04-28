from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
    path('signin/', views.SigninView.as_view(), name='custom_login'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('resend-email/<uuid:token>/', views.resend_email_verification, name='resend_email'),
]
