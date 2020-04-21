from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class calendar (models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    upcoming_events = models.CharField(max_length=200)
    def __str__(self):
        return self.upcoming_events

class Event(models.Model):
    owner = models.ForeignKey(User, null=True, unique=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_month_name = models.TextField()
    end_month_name = models.TextField(default = "")
    from_google = models.BooleanField(default=False)
    startminute = models.TextField(default="")
    endminute = models.TextField(default = "")
    starthour = models.TextField(default = "")
    endhour = models.TextField(default = "")
    @property
    def get_html_url(self):
        url = reverse('edit_event', args=(self.id,))
        return f'<a href = "{url}"> {self.title} </a>'
    def __str__(self):
        return self.title