# Generated by Django 5.0 on 2023-12-27 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiecon', '0006_remove_cartproduct_unit_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='last_submission_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
