# Generated by Django 5.1.6 on 2025-03-10 12:56

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingreso',
            name='monto_mensual',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(default=uuid.uuid4, max_length=255, unique=True),
        ),
    ]
