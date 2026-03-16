from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
    # This is a custom login view
    # path('login/', views.user_login, name='login'),

    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', next_page=reverse_lazy('shop:product_list')), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    # path('change-password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html', success_url=reverse_lazy('accounts:password_change_done')), name='change_password'),
    # path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]
