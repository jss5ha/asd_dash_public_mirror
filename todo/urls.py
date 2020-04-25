from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.addTodo, name='add'),
    path('complete/<todo_id>', views.completeTodo, name='complete'),
    path('deselect/<todo_id>', views.deselect, name='deselect'),
    path('deletecomplete', views.deleteCompleted, name='deletecomplete'),
    path('deleteall', views.deleteAll, name='deleteall'),
    path('gohome3', views.gohome3, name = "gohome3"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)