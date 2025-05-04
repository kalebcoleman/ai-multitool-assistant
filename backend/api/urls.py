from django.urls import path
from .views import NoteListCreate, NoteDelete, CreateUserView, AIQueryView, UserChatHistoryView, ClearChatHistoryView

urlpatterns = [
    path('notes/', NoteListCreate.as_view(), name='note-list-create'),
    path('notes/delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),
    path('register/', CreateUserView.as_view(), name='user-create'),
    path('query/', AIQueryView.as_view(), name='ai-query'),
    path('chat-history/', UserChatHistoryView.as_view(), name='user-chat-history'),
    path('clear-chat-history/', ClearChatHistoryView.as_view(), name='clear_chat_history'),

]
