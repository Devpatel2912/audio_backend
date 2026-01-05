from django.db import models
from accounts.models import User
from folders.models import Folder


class Audio(models.Model):
    title = models.CharField(max_length=255, blank=True, default='Audio')
    file = models.FileField(upload_to='audio/')
    duration = models.FloatField(default=0.0)
    last_played_position = models.FloatField(default=0.0)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='audios', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or "Audio"

