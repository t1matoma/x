from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    is_verified = models.BooleanField(default=False, verbose_name='Email Verified')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username



