from django.urls import path
from . import views

app_name = 'grades'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tohome/', views.go_home, name = 'gohome'),
    path('error/', views.errormeth, name='error'),
    path('courses/<int:course_id>/', views.IndCourse, name = 'toIndCourse'),
    path('courses/<int:course_id>/remove/<int:assignment_id>', views.RemoveAssignment, name = 'RemoveAssignment'),
    path('courses/<int:course_id>/remove2/<int:assignment_id>', views.RemovePointAssignment, name = 'RemovePointAssignment'),
    path('courses/NewCourse', views.NewCourse, name = 'NewCourse'),
    path('courses/RemoveCourse/<int:course_id>/', views.RemoveCourse, name = 'RemoveCourse'),
    path('courses/NewType/<int:pk>', views.NewType, name = 'NewType'),
    path('courses/RemoveType/<int:course_id>/<int:asstype_id>', views.RemoveType, name = 'RemoveType'),
    path('courses/<int:course_id>/NewAssignment/', views.NewAssignment, name = 'NewAssignment'),
    path('courses/<int:course_id>/NewAssignment2/', views.NewAssignment2, name = 'NewAssignment2'),
]