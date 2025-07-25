from django.urls import path
from . import views

urlpatterns = [
    # ========== BASIC ROUTES ==========
    path('', views.home, name='home'),                         # Landing page
    path('chat/', views.chat_view, name='chat'),               # Main Chat UI
    path('login/', views.custom_login_view, name='login'),     # Login
    path('register/', views.custom_register_view, name='register'),  # Register
    path('logout/', views.logout_view, name='logout'),         # Logout

    # ========== CHAT API ==========
    path('api/send_message/', views.send_message, name='send_message'),         # Send a message
    path('api/new_chat/', views.new_chat_session, name='new_chat_session'),      # Start a new chat
    path('api/chat_history/', views.get_chat_history, name='chat_history'),      # Get user's chat history
    path('api/session/<int:session_id>/messages/', views.load_session_messages, name='load_session_messages'),  # Load messages of a session
    path('api/rename_chat/', views.rename_chat, name='rename_chat'),             # Rename a chat session
    path('api/delete_chat/', views.delete_chat, name='delete_chat'),             # Delete a chat session
    path('api/search_chats/', views.search_chats, name='search_chats'),           # Search chat sessions

    # ========== FILE UPLOADS & GENERATION ==========
    path('api/upload_pdf/', views.upload_pdf, name='upload_pdf'),                # Upload and process PDFs
    path('api/upload_image/', views.upload_image, name='upload_image'),          # Upload and process Images
    path('api/generate_pdf/', views.generate_pdf, name='generate_pdf'),          # Generate PDF from text
    path('api/generate_ppt/', views.generate_ppt, name='generate_ppt'),          # Generate PPT from text
]
