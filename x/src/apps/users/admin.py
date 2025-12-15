"""
User admin configuration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from src.apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model"""

    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'is_verified', 'is_active', 'is_staff', 'created_at'
    ]
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'is_verified', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name')
        }),
    )
