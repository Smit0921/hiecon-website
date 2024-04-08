# Generated by Django 5.0 on 2023-12-22 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiecon', '0002_remove_customer_user_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile_no',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]