from rest_framework import serializers
from finanzas.models import (
    Usuario, Ingreso, Gasto, Activo, Deuda, TipoGasto, 
    TipoDeuda, TipoActivo, ObjetivoFinanciero, 
    PlazoFinanciero, EstrategiaFinanciera
)

# 📌 Serializador de Usuario (Protege la contraseña)
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'Nombre', 'Apellido', 'Fecha_nacimiento', 'Celular', 'Pais')

# 📌 Serializador de Ingresos con validación de montos
class IngresoSerializer(serializers.ModelSerializer):
    def validate_Monto(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto del ingreso no puede ser negativo.")
        return value

    class Meta:
        model = Ingreso
        fields = '__all__'

# 📌 Serializador de Tipo de Gasto
class TipoGastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGasto
        fields = '__all__'

# 📌 Serializador de Gastos con serialización anidada
class GastoSerializer(serializers.ModelSerializer):
    tipo_gasto = TipoGastoSerializer(read_only=True)  # Muestra el nombre del tipo de gasto

    def validate_Monto(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto del gasto no puede ser negativo.")
        return value

    class Meta:
        model = Gasto
        fields = '__all__'

# 📌 Serializador de Tipo de Activo
class TipoActivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActivo
        fields = '__all__'

# 📌 Serializador de Activos con validación
class ActivoSerializer(serializers.ModelSerializer):
    tipo_activo = TipoActivoSerializer(read_only=True)

    def validate_Monto(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto del activo no puede ser negativo.")
        return value

    class Meta:
        model = Activo
        fields = '__all__'

# 📌 Serializador de Tipo de Deuda
class TipoDeudaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDeuda
        fields = '__all__'

# 📌 Serializador de Deudas con validaciones
class DeudaSerializer(serializers.ModelSerializer):
    tipo_deuda = TipoDeudaSerializer(read_only=True)

    def validate_Monto(self, value):
        if value < 0:
            raise serializers.ValidationError("El monto de la deuda no puede ser negativo.")
        return value

    def validate_Fecha_vencimiento(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("La fecha de vencimiento no puede estar en el pasado.")
        return value

    class Meta:
        model = Deuda
        fields = '__all__'

# 📌 Serializador de Objetivos Financieros
class ObjetivoFinancieroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetivoFinanciero
        fields = '__all__'

# 📌 Serializador de Plazos Financieros
class PlazoFinancieroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlazoFinanciero
        fields = '__all__'

# 📌 Serializador de Estrategias Financieras
class EstrategiaFinancieraSerializer(serializers.ModelSerializer):
    objetivo_financiero = ObjetivoFinancieroSerializer(read_only=True)
    plazo_financiero = PlazoFinancieroSerializer(read_only=True)

    class Meta:
        model = EstrategiaFinanciera
        fields = '__all__'