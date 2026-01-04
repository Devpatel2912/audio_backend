from django.urls import path
from .views import NoteCreateView, NoteListView, NoteDetailView

urlpatterns = [
    path('', NoteCreateView.as_view(), name='note-create'),
    path('audio/<int:audio_id>/', NoteListView.as_view(), name='note-list'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
]

