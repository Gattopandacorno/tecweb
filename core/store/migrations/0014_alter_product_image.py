# Generated by Django 4.1 on 2022-08-19 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default.png', upload_to='images/'),
        ),
    ]