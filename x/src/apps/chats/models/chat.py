from django.db import models
from django.conf import settings

class ChatMember(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('chat', 'user')
        db_table = 'chat_members'

class Chat(models.Model):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ChatMember')
    last_message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.members.first()} and {self.members.last()}"
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        db_table = 'chats'
