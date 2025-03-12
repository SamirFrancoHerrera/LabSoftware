"""
URL configuration for crezco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from api.views import home  # Importamos la vista home desde api/views.py

urlpatterns = [
    path('', home, name="home"),  # Página de inicio (Esto maneja la URL raíz "/")
    path('admin/', admin.site.urls), # Ruta del panel de administración
    path('api/', include('api.urls')),  # Prefijo /api/ para la API (Esto maneja "/api/")
]