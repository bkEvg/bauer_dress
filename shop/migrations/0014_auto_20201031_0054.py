# Generated by Django 3.1 on 2020-10-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_product_price_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_to',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Цена до'),
        ),
    ]
