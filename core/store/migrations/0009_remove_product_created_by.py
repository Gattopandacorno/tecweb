# Generated by Django 4.0.5 on 2022-08-02 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_by',
        ),
    ]