from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    title = models.CharField(
        max_length=155,
        blank=True
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='chat_rooms',
        verbose_name='Участники'      
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_by_chat_rooms',
        verbose_name='Создатель'   
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

class Message(models.Model):
    chat = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='chat'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_message',
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

