# Generated by Django 3.1 on 2021-03-02 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(default='1111', max_length=1000, verbose_name='ID Платежа'),
            preserve_default=False,
        ),
    ]
