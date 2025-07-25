from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime

# Helpers for file upload paths
def upload_to_user(instance, filename):
    return f"uploads/{instance.user.username}/{filename}"

def generated_to_user(instance, filename):
    return f"generated/{instance.user.username}/{filename}"

# Custom manager for soft delete handling
class ChatSessionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# 1. Chat sessions
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = ChatSessionManager()  # Only get non-deleted chats by default
    all_objects = models.Manager()  # Access everything if needed

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.created_at.strftime('%Y-%m-%d')})"

    def rename(self, new_title):
        self.title = new_title
        self.save()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    #rember
    def get_date_group(self):
        """Return a label for grouping: 'Today', 'Yesterday', or actual date like 'April 25, 2025'."""
        now = datetime.now()
        if self.created_at.date() == now.date():
            return "Today"
        elif self.created_at.date() == (now - timedelta(days=1)).date():
            return "Yesterday"
        else:
            return self.created_at.strftime("%B %d, %Y")

# 2. Messages
class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
    )
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.role.capitalize()} @ {self.created_at.strftime('%H:%M')} - {self.content[:30]}"

# 3. Uploaded files
class UploadedFile(models.Model):
    FILE_TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('image', 'Image'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to=upload_to_user)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user.username} - {self.file_type.upper()} uploaded on {self.uploaded_at.strftime('%Y-%m-%d')}"

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

# 4. Generated files
class GeneratedFile(models.Model):
    FILE_TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('ppt', 'PPT'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_files')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to=generated_to_user)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user.username} - {self.file_type.upper()} generated on {self.created_at.strftime('%Y-%m-%d')}"

    def delete(self, *args, **kwargs):
        # Delete the file from storage
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)
