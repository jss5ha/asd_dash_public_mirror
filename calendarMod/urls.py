from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index2'),
    path('events', views.main, name = "events"),
    path('view/', views.CalendarView.as_view(), name = 'calendar'),
    path('auth', views.authorize, name = "auth"),
    path('new/', views.event, name = 'new_event'),
    path('edit/<int:event_id>', views.event, name = 'edit_event'),
]