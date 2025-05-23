# Generated by Django 5.1.6 on 2025-03-08 19:14

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjetivoFinanciero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PlazoFinanciero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoActivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDeuda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoGasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('ultimo_inicio_sesion', models.DateTimeField(blank=True, null=True)),
                ('username', models.CharField(default=uuid.uuid4, max_length=150, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='usuario_set', related_query_name='usuario', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='usuario_set', related_query_name='usuario', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_mensual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('es_variable', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Gasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo_gasto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.tipogasto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='EstrategiaFinanciera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispuesto_incrementar_ingresos', models.BooleanField(default=False)),
                ('objetivo_principal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.objetivofinanciero')),
                ('plazo_esperado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.plazofinanciero')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Deuda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_cuota', models.BooleanField(default=True)),
                ('numero_total_cuotas', models.IntegerField()),
                ('cuotas_restantes', models.IntegerField()),
                ('pago_mensual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('saldo_pendiente', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo_deuda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.tipodeuda')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Activo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_activo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('genera_ingresos_pasivos', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tipo_activo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.tipoactivo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finanzas.usuario')),
            ],
        ),
    ]
