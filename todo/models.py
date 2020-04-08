from django.db import models
import datetime
#
# GROUP_CHOICES = (
#         ('school', 'School'),
#         ('leisure', 'Leisure'),
#         ('financial', 'Financial'),
#         ('misc', 'Miscellaneous')
#     )

class Todo(models.Model):
    text = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(default=datetime.datetime.now())
    group = models.CharField(max_length=100, default="school")

    def __str__(self):
        return self.text