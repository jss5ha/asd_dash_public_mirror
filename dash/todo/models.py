from django.db import models
from django.forms import ModelForm

class Todo(models.Model):
    text = models.CharField(max_length=40)
    complete = models.BooleanField(default=False)
    # due_date = models.DateField()

    def __str__(self):
        return self.text