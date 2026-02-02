from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Folder(models.Model):
    FOLDER_TYPES = (
        ('audio', 'Audio'),
    )
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    folder_type = models.CharField(max_length=10, choices=FOLDER_TYPES, default='audio')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
