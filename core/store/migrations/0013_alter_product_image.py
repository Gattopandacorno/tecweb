# Generated by Django 4.1 on 2022-08-19 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_product_available_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]
