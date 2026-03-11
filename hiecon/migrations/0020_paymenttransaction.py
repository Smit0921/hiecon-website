from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiecon', '0019_visitor'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(help_text='Amount in rupees')),
                ('currency', models.CharField(default='INR', max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('gateway_order_id', models.CharField(blank=True, max_length=100)),
                ('gateway_payment_id', models.CharField(blank=True, max_length=100)),
                ('gateway_signature', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hiecon.cart')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hiecon.customer')),
            ],
        ),
    ]
