from django.db import models
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    physical_appearance = models.TextField(null=True, blank=True)
    interests = models.CharField(max_length=250,null=True, blank=True)
    age = models.PositiveIntegerField()
    nature = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.user}'s profile"