from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class calendar (models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    upcoming_events = models.CharField(max_length=200)
    def __str__(self):
        return self.upcoming_events