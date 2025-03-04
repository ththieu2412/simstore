# Generated by Django 5.1.6 on 2025-02-25 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_alter_district_name_alter_province_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='districts', to='locations.province'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wards', to='locations.district'),
        ),
    ]
