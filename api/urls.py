from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  # 👈 Importación correcta
from .views import (
    UsuarioViewSet, IngresoViewSet, GastoViewSet, ActivoViewSet, DeudaViewSet,
    TipoGastoViewSet, TipoDeudaViewSet, TipoActivoViewSet,
    ObjetivoFinancieroViewSet, PlazoFinancieroViewSet, EstrategiaFinancieraViewSet,
    home, CustomAuthToken
)

# 📌 Creación del router para la API
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'ingresos', IngresoViewSet)
router.register(r'gastos', GastoViewSet)
router.register(r'activos', ActivoViewSet)
router.register(r'deudas', DeudaViewSet)
router.register(r'tipo-gastos', TipoGastoViewSet)
router.register(r'tipo-deudas', TipoDeudaViewSet)
router.register(r'tipo-activos', TipoActivoViewSet)
router.register(r'objetivos-financieros', ObjetivoFinancieroViewSet)
router.register(r'plazos-financieros', PlazoFinancieroViewSet)
router.register(r'estrategias-financieras', EstrategiaFinancieraViewSet)

# 📌 Definición de las rutas
urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  
    path('api/token/', CustomAuthToken.as_view(), name='obtener-token'),  # ✅ Cambié la ruta aquí
]