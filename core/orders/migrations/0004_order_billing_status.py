# Generated by Django 4.1 on 2022-08-26 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_billing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_status',
            field=models.BooleanField(default=False),
        ),
    ]