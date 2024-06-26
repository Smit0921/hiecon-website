# Generated by Django 5.0 on 2024-03-07 09:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiecon', '0011_alter_cart_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together={('user', 'email', 'mobile_no')},
        ),
    ]
