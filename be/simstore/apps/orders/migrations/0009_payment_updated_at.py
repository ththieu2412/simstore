# Generated by Django 5.1.6 on 2025-03-10 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_payment_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
