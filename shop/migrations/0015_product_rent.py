# Generated by Django 3.1 on 2020-10-31 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20201031_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rent',
            field=models.BooleanField(default=False),
        ),
    ]
