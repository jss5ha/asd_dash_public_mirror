"""dash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from . import settings, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', include('todo.urls')),
    path('grades/', include('grades.urls')),
    path('calendar/', include('calendarMod.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('', views.home, name='home'),  # when nothing is matched, default to home inside todo/templates
    path('logout/', LogoutView.as_view(template_name=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('home/', views.home, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)