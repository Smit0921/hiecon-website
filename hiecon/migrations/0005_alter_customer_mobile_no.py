# Generated by Django 5.0 on 2023-12-22 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiecon', '0004_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile_no',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]