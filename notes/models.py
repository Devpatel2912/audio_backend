from django.db import models
from audios.models import Audio


class Note(models.Model):
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='notes')
    note_text = models.TextField()
    audio_timestamp = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['audio_timestamp']

    def __str__(self):
        return f"Note at {self.audio_timestamp}s"

