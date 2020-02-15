from django.urls import path
from . import views

app_name = 'grades'
urlpatterns = [
    path('', views.gradeHomeView.as_view(), name='grademodule'),
]