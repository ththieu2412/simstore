# Generated by Django 5.1.6 on 2025-02-18 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        ('simcards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_by', models.IntegerField()),
            ],
            options={
                'db_table': 'discount',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_order', models.IntegerField(choices=[(0, 'Đã hủy'), (1, 'Chờ xác nhận'), (2, 'Đang giao hàng'), (3, 'Đã giao hàng')], default=1)),
                ('payment_methods', models.CharField(choices=[('Cash', 'Cash'), ('Bank Card', 'Bank Card')], max_length=50)),
                ('detailed_address', models.CharField(max_length=255)),
                ('note', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.customer')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.discount')),
                ('sim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simcards.sim')),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.ward')),
            ],
            options={
                'db_table': 'order',
            },
        ),
    ]
