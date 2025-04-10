from rest_framework import serializers
from finanzas.models import (
    Usuario, Ingreso, Gasto, Activo, Deuda
)

# 📌 Serializador de Usuario (Protege la contraseña)
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'Nombre', 'Apellido', 'Fecha_nacimiento')

# 📌 Serializador de Ingresos con validación de montos
class IngresoSerializer(serializers.ModelSerializer):
    def validate_Monto(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto del ingreso no puede ser negativo.")
        return value

    class Meta:
        model = Ingreso
        fields = '__all__'



# 📌 Serializador de Gastos con serialización anidada
class GastoSerializer(serializers.ModelSerializer):
    def validate_Monto(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto del gasto no puede ser negativo.")
        return value

    class Meta:
        model = Gasto
        fields = '__all__'



# 📌 Serializador de Activos con validación
class ActivoSerializer(serializers.ModelSerializer):
    def validate_Monto(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto del activo no puede ser negativo.")
        return value

    class Meta:
        model = Activo
        fields = '__all__'



# 📌 Serializador de Deudas con validaciones
class DeudaSerializer(serializers.ModelSerializer):
    def validate_Monto(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto de la deuda no puede ser negativo.")
        return value

    #def validate_Fecha_vencimiento(self, value):
    #    from datetime import date
    #    if value < date.today():
    #        raise serializers.ValidationError("La fecha de vencimiento no puede estar en el pasado.")
    #    return value

    class Meta:
        model = Deuda
        fields = '__all__'

