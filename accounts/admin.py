from django.contrib import admin

from .models import CustomUser, Profile



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email',]
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    ordering = ['email']



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']