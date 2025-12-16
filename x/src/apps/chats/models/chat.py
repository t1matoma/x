from django.db import models
from django.conf import settings

class Chat(models.Model):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    last_message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.members.first()} and {self.members.last()}"
    class Meta:
        ordering = ['-timestamp']
        unique_together = ('members',)
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        db_table = 'chats'
