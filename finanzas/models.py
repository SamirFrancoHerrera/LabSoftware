from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid


def validate_positive(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is not a positive number'),
            params={'value': value},
        )
    
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_inicio_sesion = models.DateTimeField(null=True, blank=True)
    username = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Cambia el related_name para evitar conflictos
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_set',  # Cambia el related_name para evitar conflictos
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='usuario',
    )

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.nombre} {self.apellido}'

    def get_short_name(self):
        return self.nombre

# 📌 Modelo de Ingresos
class Ingreso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto_mensual = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])
    es_variable = models.BooleanField(default=False)  # Indica si es ingreso fijo o variable

    def __str__(self):
        return f'{self.monto_mensual:.2f}'

# 📌 Modelo de Gastos
class TipoGasto(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Gasto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_gasto = models.ForeignKey(TipoGasto, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])

    def __str__(self):
        return f'{self.monto:.2f}'

# 📌 Modelo de Deudas
class TipoDeuda(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Deuda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_deuda = models.ForeignKey(TipoDeuda, on_delete=models.CASCADE)
    tipo_cuota = models.BooleanField(default=True)  # True: fija, False: variable
    numero_total_cuotas = models.IntegerField()
    cuotas_restantes = models.IntegerField()
    pago_mensual = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])

    def clean(self):
        ingresos = Ingreso.objects.filter(usuario=self.usuario)
        if ingresos.exists():
            ingreso_mensual = ingresos.aggregate(models.Sum('monto_mensual'))['monto_mensual__sum']
            if self.pago_mensual > ingreso_mensual:
                raise ValidationError(_('La cuota de la deuda no puede ser mayor que el ingreso mensual del usuario.'))

    def __str__(self):
        return f'{self.saldo_pendiente:.2f}'

# 📌 Modelo de Activos
class TipoActivo(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Activo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_activo = models.ForeignKey(TipoActivo, on_delete=models.CASCADE)
    valor_activo = models.DecimalField(max_digits=10, decimal_places=2)
    genera_ingresos_pasivos = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.valor_activo:.2f}'

# 📌 Modelo de Estrategia Financiera
class ObjetivoFinanciero(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class PlazoFinanciero(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion

class EstrategiaFinanciera(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    objetivo_principal = models.ForeignKey(ObjetivoFinanciero, on_delete=models.CASCADE)
    plazo_esperado = models.ForeignKey(PlazoFinanciero, on_delete=models.CASCADE)
    dispuesto_incrementar_ingresos = models.BooleanField(default=False)

    def __str__(self):
        return self.objetivo_principal.nombre