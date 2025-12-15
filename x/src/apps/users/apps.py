"""
User app configuration
"""
from django.apps import AppConfig

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.users'
    verbose_name = 'Users'
