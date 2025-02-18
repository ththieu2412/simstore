# Generated by Django 5.1.6 on 2025-02-18 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('simcards', '0001_initial'),
        ('suppliers', '0002_alter_importreceiptdetail_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importreceipt',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='importReceipt', to='accounts.employee'),
        ),
        migrations.AlterField(
            model_name='importreceiptdetail',
            name='sim_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='importReceiptDetail', to='simcards.sim'),
        ),
    ]
