# Generated by Django 5.1.6 on 2025-02-18 08:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImportReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('employee_id', models.IntegerField()),
            ],
            options={
                'db_table': 'importReceipt',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'supplier',
            },
        ),
        migrations.CreateModel(
            name='ImportReceiptDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sim_id', models.IntegerField()),
                ('import_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('import_receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.importreceipt')),
            ],
            options={
                'db_table': 'importReceiptDetail',
            },
        ),
        migrations.AddField(
            model_name='importreceipt',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.supplier'),
        ),
    ]
