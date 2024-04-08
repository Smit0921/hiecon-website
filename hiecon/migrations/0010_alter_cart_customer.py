# Generated by Django 5.0 on 2024-01-04 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiecon', '0009_alter_cartproduct_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hiecon.customer', unique=True),
        ),
    ]