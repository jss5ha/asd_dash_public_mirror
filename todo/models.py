from django.db import models
import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm

class Todo(models.Model):
    owner = models.ForeignKey(User,null=True, unique=False, on_delete=models.CASCADE)
    text = models.CharField(max_length=40)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return self.text