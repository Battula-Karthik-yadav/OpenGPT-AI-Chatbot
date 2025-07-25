from django.contrib import admin
from .models import ChatSession, ChatMessage, UploadedFile, GeneratedFile

# --- Inline for ChatMessage inside ChatSession ---
class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 1  # How many empty forms to show
    fields = ('role', 'content', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True

# --- ChatSession Admin ---
@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('user__username', 'title')
    ordering = ('-created_at',)
    inlines = [ChatMessageInline]  # <-- This adds the messages inline!

# --- ChatMessage Admin ---
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('session__title', 'content')
    ordering = ('-created_at',)

# --- UploadedFile Admin ---
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file_type', 'file', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('user__username', 'file')
    ordering = ('-uploaded_at',)

# --- GeneratedFile Admin ---
@admin.register(GeneratedFile)
class GeneratedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file_type', 'file', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('user__username', 'file')
    ordering = ('-created_at',)
