# Crezco - Tu Plataforma de Gestión Financiera Personal

¡Bienvenido a Crezco, tu solución integral para administrar tus finanzas personales!

## Descripción

Crezco es una aplicación web desarrollada con Django que te permite gestionar tus ingresos, gastos, deudas, activos y estrategias financieras en un solo lugar.

## Características Principales

* **Gestión de Ingresos:** Registra tus ingresos mensuales, tanto fijos como variables.
* **Seguimiento de Gastos:** Clasifica tus gastos por categorías y visualiza tus patrones de gasto.
* **Control de Deudas:** Mantén un registro de tus deudas, pagos y saldos pendientes.
* **Administración de Activos:** Lleva un seguimiento de tus activos y su valor.
* **Planificación Financiera:** Define tus objetivos financieros y crea estrategias para alcanzarlos.
* **Usuarios:** Los usuarios pueden registrarse, iniciar sesión y administrar sus datos financieros de forma segura.

## Modelos de Datos

* **Usuario:** Representa a los usuarios del sistema.
* **Ingreso:** Registra los ingresos de un usuario.
* **Gasto:** Registra los gastos de un usuario, clasificados por categorías.
* **Deuda:** Registra las deudas de un usuario, incluyendo pagos y saldos pendientes.
* **Activo:** Registra los activos de un usuario y su valor.
* **EstrategiaFinanciera:** Define los objetivos y estrategias financieras de un usuario.
* **TipoGasto:** Define las categorías de gastos.
* **TipoDeuda:** Define los tipos de deudas.
* **TipoActivo:** Define los tipos de activos.
* **ObjetivoFinanciero:** Define los objetivos financieros.
* **PlazoFinanciero:** Define los plazos financieros.

## Requisitos

* Python 3.x
* Django 4.x
* PostgreSQL (o cualquier base de datos compatible con Django)
* Docker (opcional, para desarrollo en contenedores)

## Instalación

1.  Clona el repositorio:

    ```bash
    git clone https://github.com/SamirFrancoHerrera/LabSoftware
    cd crezco
    ```

2.  Crea un entorno virtual (opcional):

    ```bash
    python -m venv venv
    source venv/bin/activate # En Linux/macOS
    venv\Scripts\activate # En Windows
    ```

3.  Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4.  Configura la base de datos en `crezco/settings.py`.

5.  Ejecuta las migraciones:

    ```bash
    python manage.py migrate
    ```

6.  Crea un superusuario:

    ```bash
    python manage.py createsuperuser
    ```

7.  Ejecuta el servidor de desarrollo:

    ```bash
    python manage.py runserver
    ```

## Diagrama de Clases

```mermaid
classDiagram
    class Usuario {
        - email: EmailField
        - nombre: CharField
        - apellido: CharField
        - fecha_registro: DateTimeField
        - ultimo_inicio_sesion: DateTimeField
        - username: CharField
        + __str__(): str
        + get_full_name(): str
        + get_short_name(): str
    }

    class Ingreso {
        - monto_mensual: DecimalField
        - es_variable: BooleanField
        + __str__(): str
    }

    class TipoGasto {
        - nombre: CharField
        + __str__(): str
    }

    class Gasto {
        - monto: DecimalField
        + __str__(): str
    }

    class TipoDeuda {
        - nombre: CharField
        + __str__(): str
    }

    class Deuda {
        - tipo_cuota: BooleanField
        - numero_total_cuotas: IntegerField
        - cuotas_restantes: IntegerField
        - pago_mensual: DecimalField
        - saldo_pendiente: DecimalField
        + __str__(): str
    }

    class TipoActivo {
        - nombre: CharField
        + __str__(): str
    }

    class Activo {
        - valor_activo: DecimalField
        - genera_ingresos_pasivos: DecimalField
        + __str__(): str
    }

    class ObjetivoFinanciero {
        - nombre: CharField
        + __str__(): str
    }

    class PlazoFinanciero {
        - descripcion: CharField
        + __str__(): str
    }

    class EstrategiaFinanciera {
        - dispuesto_incrementar_ingresos: BooleanField
        + __str__(): str
    }

    Usuario "1..*" -- "1" Ingreso : tiene
    Usuario "1..*" -- "1" Gasto : tiene
    Usuario "1..*" -- "1" Deuda : tiene
    Usuario "1..*" -- "1" Activo : tiene
    Usuario "1..*" -- "1" EstrategiaFinanciera : tiene

    TipoGasto "1" -- "1..*" Gasto : tipos
    TipoDeuda "1" -- "1..*" Deuda : tipos
    TipoActivo "1" -- "1..*" Activo : tipos
    ObjetivoFinanciero "1" -- "1" EstrategiaFinanciera : objetivos
    PlazoFinanciero "1" -- "1" EstrategiaFinanciera : plazos

    Deuda "1" -- "1" Usuario : usuario
    Gasto "1" -- "1" Usuario : usuario
    Ingreso "1" -- "1" Usuario : usuario
    Activo "1" -- "1" Usuario : usuario
    EstrategiaFinanciera "1" -- "1" Usuario : usuario