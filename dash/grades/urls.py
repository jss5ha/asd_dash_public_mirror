from django.urls import path
from . import views

app_name = 'grades'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('courses/', views.CourseView.as_view(), name = 'courses'),
    path('courses/<int:pk>/', views.IndCourse, name = 'toIndCourse'),
    path('courses/NewCourse', views.NewCourse, name = 'NewCourse'),
    path('assignmentlist/', views.assView.as_view(), name = 'Assignment View'),
    path('assignments/', views.addAssignmentView.as_view(), name = 'addAssignment'),
   
]