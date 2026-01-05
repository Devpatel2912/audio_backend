from django.db import models
from accounts.models import User
from folders.models import Folder


class Pdf(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdf/')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='pdfs', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdfs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
