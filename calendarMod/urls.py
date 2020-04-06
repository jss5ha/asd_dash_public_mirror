from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('events', views.main, name = "events"),
    path('calview', views.CalendarView.as_view(), name = 'calendar'),
]