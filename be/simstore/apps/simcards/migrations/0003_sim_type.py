# Generated by Django 5.1.6 on 2025-03-05 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simcards', '0002_alter_sim_export_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='sim',
            name='type',
            field=models.CharField(choices=[('physical', 'Sim vật lý'), ('qr', 'QR Sim')], default='physical', max_length=10),
        ),
    ]
