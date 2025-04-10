from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('agregar_transaccion/', views.agregar_transaccion, name='agregar_transaccion'),
]