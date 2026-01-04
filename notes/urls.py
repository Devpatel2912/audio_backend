from django.urls import path
from .views import NoteCreateView, NoteListView, NoteDetailView, PdfNoteListView

urlpatterns = [
    path('', NoteCreateView.as_view(), name='note-create'),
    path('audio/<int:audio_id>/', NoteListView.as_view(), name='note-list'),
    path('pdf/<int:pdf_id>/', PdfNoteListView.as_view(), name='pdf-note-list'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
]

