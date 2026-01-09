from django.db import models
from accounts.models import User
from folders.models import Folder


def audio_upload_path(instance, filename):
    folder_path = ''
    if instance.folder:
        # Sanitize the folder name
        safe_name = "".join([c for c in instance.folder.name if c.isalnum() or c in " ._-"])
        # Avoid empty string if sanitization strips everything
        if safe_name:
             folder_path = f'{safe_name}/'
    
    return f'audio/{instance.user.id}/{folder_path}{filename}'


class Audio(models.Model):
    title = models.CharField(max_length=255, blank=True, default='Audio')
    audio_file = models.FileField(upload_to=audio_upload_path)
    duration = models.FloatField(default=0.0)
    last_played_position = models.FloatField(default=0.0)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='audios', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or "Audio"

