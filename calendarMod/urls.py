from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index2'),
    path('events', views.main, name = "events"),
    path('view/', views.CalendarView.as_view(), name = 'calendar'),
    path('auth', views.authorize, name = "auth"),
    path('new/', views.event, name = 'new_event'),
    path('edit/<int:event_id>', views.event, name = 'edit_event'),
    path('delete/', views.deleteall, name = 'delete_all'),
    path('delete/<int:event_id>', views.delete_event, name = 'delete_event'),
    path('gohome2', views.gohome2, name = "gohome2"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)