# Generated by Django 5.1.7 on 2025-03-29 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simcards', '0007_sim_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sim',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='sim',
            name='type',
        ),
    ]
