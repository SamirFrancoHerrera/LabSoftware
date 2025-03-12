from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate

from finanzas.models import (
    Usuario, Ingreso, Gasto, Activo, Deuda, TipoGasto,
    TipoDeuda, TipoActivo, ObjetivoFinanciero, PlazoFinanciero, EstrategiaFinanciera
)

from .serializers import (
    UsuarioSerializer, IngresoSerializer, GastoSerializer,
    ActivoSerializer, DeudaSerializer, TipoGastoSerializer,
    TipoDeudaSerializer, TipoActivoSerializer,
    ObjetivoFinancieroSerializer, PlazoFinancieroSerializer,
    EstrategiaFinancieraSerializer
)

# 📌 Página de bienvenida a la API
@csrf_exempt
def home(request):
    return JsonResponse({"message": "¡Bienvenido a Crezco API!"})

# 📌 Autenticación personalizada para obtener el token de usuario
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id, 'email': user.email})
        else:
            return Response({'error': 'Credenciales inválidas'}, status=400)

# 📌 ViewSet para Usuarios
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

# 📌 ViewSet para Ingresos con filtros
class IngresoViewSet(viewsets.ModelViewSet):
    queryset = Ingreso.objects.all()
    serializer_class = IngresoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['Monto']
    search_fields = ['usuario__email']

    def get_queryset(self):
        return Ingreso.objects.filter(usuario=self.request.user)

# 📌 ViewSet para Gastos
class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Gasto.objects.filter(usuario=self.request.user)

# 📌 ViewSet para Activos
class ActivoViewSet(viewsets.ModelViewSet):
    queryset = Activo.objects.all()
    serializer_class = ActivoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Activo.objects.filter(usuario=self.request.user)

# 📌 ViewSet para Deudas
class DeudaViewSet(viewsets.ModelViewSet):
    queryset = Deuda.objects.all()
    serializer_class = DeudaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Deuda.objects.filter(usuario=self.request.user)

# 📌 ViewSet para Tipos de Gasto
class TipoGastoViewSet(viewsets.ModelViewSet):
    queryset = TipoGasto.objects.all()
    serializer_class = TipoGastoSerializer
    permission_classes = [IsAuthenticated]

# 📌 ViewSet para Tipos de Activo
class TipoActivoViewSet(viewsets.ModelViewSet):
    queryset = TipoActivo.objects.all()
    serializer_class = TipoActivoSerializer
    permission_classes = [IsAuthenticated]

# 📌 ViewSet para Tipos de Deuda
class TipoDeudaViewSet(viewsets.ModelViewSet):
    queryset = TipoDeuda.objects.all()
    serializer_class = TipoDeudaSerializer
    permission_classes = [IsAuthenticated]

# 📌 ViewSet para Objetivos Financieros
class ObjetivoFinancieroViewSet(viewsets.ModelViewSet):
    queryset = ObjetivoFinanciero.objects.all()
    serializer_class = ObjetivoFinancieroSerializer
    permission_classes = [IsAuthenticated]

# 📌 ViewSet para Plazos Financieros
class PlazoFinancieroViewSet(viewsets.ModelViewSet):
    queryset = PlazoFinanciero.objects.all()
    serializer_class = PlazoFinancieroSerializer
    permission_classes = [IsAuthenticated]

# 📌 ViewSet para Estrategias Financieras
class EstrategiaFinancieraViewSet(viewsets.ModelViewSet):
    queryset = EstrategiaFinanciera.objects.all()
    serializer_class = EstrategiaFinancieraSerializer
    permission_classes = [IsAuthenticated]