from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm

#
# GROUP_CHOICES = (
#         ('school', 'School'),
#         ('leisure', 'Leisure'),
#         ('financial', 'Financial'),
#         ('misc', 'Miscellaneous')
#     )

class Todo(models.Model):
    owner = models.ForeignKey(User, null=True, unique=False, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.datetime.now)
    group = models.CharField(max_length=100, default="school")

    def __str__(self):
        return self.text
