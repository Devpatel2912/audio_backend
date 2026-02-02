from django.db import models
from audios.models import Audio




class Note(models.Model):
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='notes', null=True, blank=True)

    note_text = models.TextField()
    audio_timestamp = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        if self.audio:
            return f"Note on Audio at {self.audio_timestamp}s"

        return "Note"

