# Generated by Django 4.1 on 2022-08-11 09:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_review_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=4.5, max_digits=4, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.PositiveIntegerField(choices=[(1, '1 - Trash'), (2, '2 - Bad'), (3, '3 - Ok'), (4, '4 - Nice'), (5, '5 - Perfect')]),
        ),
    ]