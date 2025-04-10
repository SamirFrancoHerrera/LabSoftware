# Generated by Django 5.2 on 2025-04-10 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0005_alter_gasto_tipo_gasto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activo',
            name='tipo_activo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finanzas.tipoactivo'),
        ),
        migrations.AlterField(
            model_name='deuda',
            name='tipo_deuda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finanzas.tipodeuda'),
        ),
    ]
