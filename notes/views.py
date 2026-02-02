from rest_framework import generics
from django.db import models
from .models import Note
from audios.models import Audio
from .serializers import NoteSerializer, NoteCreateSerializer




class NoteCreateView(generics.CreateAPIView):
    serializer_class = NoteCreateSerializer


class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        audio_id = self.kwargs.get('audio_id')
        try:
            audio = Audio.objects.get(id=audio_id, user=self.request.user)
            return Note.objects.filter(audio=audio)
        except Audio.DoesNotExist:
            return Note.objects.none()




class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(audio__user=user)

