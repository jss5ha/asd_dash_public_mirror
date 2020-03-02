from django.db import models
import datetime

class Todo(models.Model):
    text = models.CharField(max_length=40)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return self.text