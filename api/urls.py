from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet, basename='usuarios')
router.register(r'ingresos', views.IngresoViewSet, basename='ingresos')
router.register(r'gastos', views.GastoViewSet, basename='gastos')
router.register(r'activos', views.ActivoViewSet, basename='activos')
router.register(r'deudas', views.DeudaViewSet, basename='deudas')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.CustomAuthToken.as_view(), name='obtener-token'),
    ]