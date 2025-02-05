from django.db import models

# Create your models here.

class ChatSession(models.Model):
    thread_id = models.CharField(max_length=255, unique=True)
    # Stores the conversation as a JSON list (each item is a dict with "role" and "content")
    conversation = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatSession {self.thread_id} at {self.created_at}"
