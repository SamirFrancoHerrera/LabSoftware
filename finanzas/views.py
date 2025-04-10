from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Ingreso, Gasto, Activo, Deuda
from django.db import models

def dashboard(request):
    return render(request, 'finanzas/dashboard.html')

@csrf_exempt
def agregar_transaccion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tipo_transaccion = data.get('tipo_transaccion')

            if tipo_transaccion == 'ingreso':
                monto_mensual = data['montoMensual']  # Asegúrate de que la clave coincida con el envío JS
                es_variable = data['esVariable']    # Asegúrate de que la clave coincida con el envío JS
                if request.user.is_authenticated:
                    Ingreso.objects.create(usuario=request.user, monto_mensual=monto_mensual, es_variable=es_variable)
                    mensaje = 'Ingreso agregado con éxito.'
                    success = True
                else:
                    mensaje = 'Usuario no autenticado.'
                    success = False
            elif tipo_transaccion == 'gasto':
                monto = float(data.get('monto', 0))
                if request.user.is_authenticated:
                    Gasto.objects.create(usuario=request.user, monto=monto)
                    mensaje = 'Gasto agregado con éxito.'
                    success = True
                else:
                    mensaje = 'Usuario no autenticado.'
                    success = False
            elif tipo_transaccion == 'activo':
                valor_activo = data['valorActivo']
                genera_ingresos_pasivos = data['generaIngresosPasivos']
                if request.user.is_authenticated:
                    Activo.objects.create(usuario=request.user, genera_ingresos_pasivos=genera_ingresos_pasivos, valor_activo=valor_activo)
                    mensaje = 'Activo agregado con éxito.'
                    success = True
                else:
                    mensaje = 'Usuario no autenticado.'
                    success = False
            elif tipo_transaccion == 'deuda':
                tipo_cuota = data['tipo_cuota'] == 'true'  # Convertir string a booleano
                numero_total_cuotas = int(data['numero_total_cuotas'])
                cuotas_restantes = int(data['cuotas_restantes'])
                pago_mensual = float(data['pago_mensual'])
                saldo_pendiente = float(data['saldo_pendiente'])
                if request.user.is_authenticated:
                    Deuda.objects.create(usuario=request.user, tipo_cuota=tipo_cuota, numero_total_cuotas=numero_total_cuotas,cuotas_restantes=cuotas_restantes, pago_mensual=pago_mensual, saldo_pendiente=saldo_pendiente)
                    mensaje = 'Deuda agregada con éxito.'
                    success = True
                else:
                    mensaje = 'Usuario no autenticado.'
                    success = False
            else:
                mensaje = 'Tipo de transacción no válido.'
                success = False

            # Obtener datos actualizados para la gráfica
            ingresos_total = Ingreso.objects.filter(usuario=request.user).aggregate(total_ingresos=models.Sum('monto_mensual'))['total_ingresos'] or 0
            gastos_total = Gasto.objects.filter(usuario=request.user).aggregate(total_gastos=models.Sum('monto'))['total_gastos'] or 0

            dashboard_data = {
                'ingresos_total': float(ingresos_total),
                'gastos_total': float(gastos_total),
                'activos_total': Activo.objects.filter(usuario=request.user).aggregate(total_activos=models.Sum('valor_activo'))['total_activos'] or 0,
                'deudas_total': Deuda.objects.filter(usuario=request.user).aggregate(total_deudas=models.Sum('saldo_pendiente'))['total_deudas'] or 0,
                # Aquí podrías agregar más datos para la gráfica (ej: lista de transacciones recientes)
            }

            return JsonResponse({'success': success, 'message': mensaje, 'dashboard_data': dashboard_data})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al agregar la transacción: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)
    

