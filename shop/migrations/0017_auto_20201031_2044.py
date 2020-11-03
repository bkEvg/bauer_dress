# Generated by Django 3.1 on 2020-10-31 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_auto_20201031_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.AlterField(
            model_name='product',
            name='rent',
            field=models.BooleanField(default=False, verbose_name='Доступно в аренду (если да, заполни ниже)'),
        ),
    ]
