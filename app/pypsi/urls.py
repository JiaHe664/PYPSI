"""pypsi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin", admin.site.urls),
    path("client", views.client_home),
    path('login', views.login),   
    path("client/upload", views.client_upload),
    path("client/download/<str:filename>", views.client_download),
    path("client/deleteTable/<str:filename>", views.client_deleteTable),
    path("client/deleteResult/<str:filename>", views.client_deleteResult),
    path('client/loadTable', views.client_loadTable),
    path('client/loadTask', views.client_loadTask),
    path('client/loadResult', views.client_loadResult),
    path('client/createTask', views.client_createTask),
    path('client/startTask', views.client_startTask),
    path('server/startTask', views.server_startTask),  
    path('client/showDetails', views.showDetails), 
    
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
