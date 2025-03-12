from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from finanzas.models import Ingreso, Gasto, TipoGasto, Deuda, TipoDeuda, Activo, TipoActivo, EstrategiaFinanciera, ObjetivoFinanciero, PlazoFinanciero

Usuario = get_user_model()

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            nombre='Test',
            apellido='User'
        )

    def test_usuario_creation(self):
        self.assertEqual(self.usuario.email, 'test@example.com')
        self.assertEqual(self.usuario.nombre, 'Test')
        self.assertEqual(self.usuario.apellido, 'User')
        self.assertTrue(self.usuario.check_password('password123'))

    def test_superuser_creation(self):
        superuser = Usuario.objects.create_superuser(
            username='adminuser',
            email="admin@example.com",
            password="adminpassword",
            nombre="Admin",
            apellido="User"
        )
        self.assertTrue(superuser.is_superuser)

    def test_superusuario_str(self):
        self.assertEqual(str(self.usuario), 'test@example.com')

    def test_usuario_full_name(self):
        self.assertEqual(self.usuario.get_full_name(), 'Test User')

    def test_contrasena_hash(self):
        self.assertTrue(self.usuario.check_password('password123'))
        self.assertFalse(self.usuario.check_password('wrongpassword'))

    def test_password_validation(self):
        # Contraseña demasiado corta
        with self.assertRaises(ValidationError):
            validate_password('short', self.usuario)

        # Contraseña común
        with self.assertRaises(ValidationError):
            validate_password('password', self.usuario)

        # Contraseña solo numérica
        with self.assertRaises(ValidationError):
            validate_password('12345678', self.usuario)

        # Contraseña válida
        try:
            validate_password('ValidPassword123', self.usuario)
        except ValidationError:
            self.fail('validate_password() raised ValidationError unexpectedly!')

class IngresoModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            nombre='Test',
            apellido='User'
        )
        self.ingreso = Ingreso.objects.create(
            usuario=self.usuario,
            monto_mensual=1000.00,
            es_variable=False
        )

    def test_ingreso_creation(self):
        self.assertEqual(self.ingreso.usuario, self.usuario)
        self.assertEqual(self.ingreso.monto_mensual, 1000.00)
        self.assertFalse(self.ingreso.es_variable)

    def test_ingreso_str(self):
        self.assertEqual(str(self.ingreso), '1000.00')

    def test_relacion_usuario(self):
        self.assertEqual(self.ingreso.usuario, self.usuario)

    def test_monto_mensual_no_negativo(self):
        with self.assertRaises(ValidationError):
            ingreso_negativo = Ingreso(
                usuario=self.usuario,
                monto_mensual=-1000.00,
                es_variable=False
            )
            ingreso_negativo.full_clean()  # Esto ejecuta las validaciones del modelo

class GastoModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            nombre='Test',
            apellido='User'
        )
        self.tipo_gasto = TipoGasto.objects.create(nombre='Alquiler')
        self.gasto = Gasto.objects.create(
            usuario=self.usuario,
            tipo_gasto=self.tipo_gasto,
            monto=500.00
        )

    def test_gasto_creation(self):
        self.assertEqual(self.gasto.usuario, self.usuario)
        self.assertEqual(self.gasto.tipo_gasto, self.tipo_gasto)
        self.assertEqual(self.gasto.monto, 500.00)

    def test_gasto_str(self):
        self.assertEqual(str(self.gasto), '500.00')

    def test_gasto_usuario_relation(self):
        self.assertEqual(self.gasto.usuario.email, 'test@example.com')

    def test_monto_no_negativo(self):
        with self.assertRaises(ValidationError):
            gasto_negativo = Gasto(
                usuario=self.usuario,
                tipo_gasto=self.tipo_gasto,
                monto=-500.00
            )
            gasto_negativo.full_clean()  # Esto ejecuta las validaciones del modelo

class DeudaModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            nombre='Test',
            apellido='User'
        )
        self.tipo_deuda = TipoDeuda.objects.create(nombre='Hipoteca')
        self.deuda = Deuda.objects.create(
            usuario=self.usuario,
            tipo_deuda=self.tipo_deuda,
            tipo_cuota=True,
            numero_total_cuotas=360,
            cuotas_restantes=350,
            pago_mensual=1500.00,
            saldo_pendiente=525000.00
        )

    def test_deuda_creation(self):
        self.assertEqual(self.deuda.usuario, self.usuario)
        self.assertEqual(self.deuda.tipo_deuda, self.tipo_deuda)
        self.assertTrue(self.deuda.tipo_cuota)
        self.assertEqual(self.deuda.numero_total_cuotas, 360)
        self.assertEqual(self.deuda.cuotas_restantes, 350)
        self.assertEqual(self.deuda.pago_mensual, 1500.00)
        self.assertEqual(self.deuda.saldo_pendiente, 525000.00)

    def test_deuda_str(self):
        self.assertEqual(str(self.deuda), '525000.00')

    def test_deuda_usuario_relation(self):
        self.assertEqual(self.deuda.usuario.email, 'test@example.com')

    def test_cuota_no_mayor_ingreso(self):
        # Crear un ingreso para el usuario
        Ingreso.objects.create(
            usuario=self.usuario,
            monto_mensual=1000.00,
            es_variable=False
        )

        with self.assertRaises(ValidationError):
            deuda_invalida = Deuda(
                usuario=self.usuario,
                tipo_deuda=self.tipo_deuda,
                tipo_cuota=True,
                numero_total_cuotas=360,
                cuotas_restantes=350,
                pago_mensual=2000.00,  # Mayor que el ingreso mensual del usuario
                saldo_pendiente=525000.00
            )
            deuda_invalida.full_clean()  # Esto ejecuta las validaciones del modelo

class ActivoModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            nombre='Test',
            apellido='User'
        )
        self.tipo_activo = TipoActivo.objects.create(nombre='Inmueble')
        self.activo = Activo.objects.create(
            usuario=self.usuario,
            tipo_activo=self.tipo_activo,
            valor_activo=300000.00,
            genera_ingresos_pasivos=2000.00
        )

    def test_activo_creation(self):
        self.assertEqual(self.activo.usuario, self.usuario)
        self.assertEqual(self.activo.tipo_activo, self.tipo_activo)
        self.assertEqual(self.activo.valor_activo, 300000.00)
        self.assertEqual(self.activo.genera_ingresos_pasivos, 2000.00)

    def test_activo_str(self):
        self.assertEqual(str(self.activo), '300000.00')

    def test_activo_usuario_relation(self):
        self.assertEqual(self.activo.usuario.email, 'test@example.com')

class EstrategiaFinancieraModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            nombre='Test',
            apellido='User'
        )
        self.objetivo_financiero = ObjetivoFinanciero.objects.create(nombre='Ahorro')
        self.plazo_financiero = PlazoFinanciero.objects.create(descripcion='5 años')
        self.estrategia_financiera = EstrategiaFinanciera.objects.create(
            usuario=self.usuario,
            objetivo_principal=self.objetivo_financiero,
            plazo_esperado=self.plazo_financiero,
            dispuesto_incrementar_ingresos=True
        )

    def test_estrategia_financiera_creation(self):
        self.assertEqual(self.estrategia_financiera.usuario, self.usuario)
        self.assertEqual(self.estrategia_financiera.objetivo_principal, self.objetivo_financiero)
        self.assertEqual(self.estrategia_financiera.plazo_esperado, self.plazo_financiero)
        self.assertTrue(self.estrategia_financiera.dispuesto_incrementar_ingresos)

    def test_estrategia_financiera_str(self):
        self.assertEqual(str(self.estrategia_financiera), 'Ahorro')

    def test_estrategia_financiera_usuario_relation(self):
        self.assertEqual(self.estrategia_financiera.usuario.email, 'test@example.com')

