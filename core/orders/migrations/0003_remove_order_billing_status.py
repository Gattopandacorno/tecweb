# Generated by Django 4.1 on 2022-08-26 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_status',
        ),
    ]
