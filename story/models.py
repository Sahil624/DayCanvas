from django.db import models
from django.contrib.auth import get_user_model


class Journal(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_created=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    journal = models.TextField()

def upload_to(instance, filename):
    username = instance.journal.user.username
    return f'images/{username}/{filename}'

class JournalImages(models.Model):
    journal = models.ForeignKey(Journal, related_name='images', on_delete=models.CASCADE)
    file = models.ImageField(upload_to=upload_to)