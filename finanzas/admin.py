from django.contrib import admin
from .models import Usuario, Ingreso, TipoGasto, Gasto, TipoDeuda, Deuda, TipoActivo, Activo, ObjetivoFinanciero, PlazoFinanciero, EstrategiaFinanciera

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Ingreso)
admin.site.register(TipoGasto)
admin.site.register(Gasto)
admin.site.register(TipoDeuda)
admin.site.register(Deuda)
admin.site.register(TipoActivo)
admin.site.register(Activo)
admin.site.register(ObjetivoFinanciero)
admin.site.register(PlazoFinanciero)
admin.site.register(EstrategiaFinanciera)