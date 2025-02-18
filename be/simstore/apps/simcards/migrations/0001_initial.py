# Generated by Django 5.1.6 on 2025-02-18 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'category1',
            },
        ),
        migrations.CreateModel(
            name='Category2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'category2',
            },
        ),
        migrations.CreateModel(
            name='MobileNetworkOperator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'mobileNetworkOperator',
            },
        ),
        migrations.CreateModel(
            name='SIM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('export_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simcards.category1')),
                ('category_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simcards.category2')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.employee')),
                ('mobile_network_operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simcards.mobilenetworkoperator')),
            ],
            options={
                'db_table': 'sim',
            },
        ),
    ]
