# Generated by Django 3.1 on 2020-11-06 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_simple_coupons.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedUsersRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_users', models.BooleanField(default=False, verbose_name='Все пользователи?')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Пользователи')),
            ],
            options={
                'verbose_name': 'правило разрешений',
                'verbose_name_plural': 'правила разрешений',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=django_simple_coupons.helpers.get_random_code, max_length=12, unique=True, verbose_name='Код купона')),
                ('times_used', models.IntegerField(default=0, editable=False, verbose_name='Использовано (раз)')),
                ('created', models.DateTimeField(editable=False, verbose_name='Создан')),
            ],
            options={
                'verbose_name': 'купон',
                'verbose_name_plural': 'купоны',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0, verbose_name='Значение')),
                ('is_percentage', models.BooleanField(default=False, verbose_name='В процентах?')),
            ],
            options={
                'verbose_name': 'скидка',
                'verbose_name_plural': 'скидки',
            },
        ),
        migrations.CreateModel(
            name='MaxUsesRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_uses', models.BigIntegerField(default=0, verbose_name='Макс. кол-во использований')),
                ('is_infinite', models.BooleanField(default=False, verbose_name='Бесконечные использования?')),
                ('uses_per_user', models.IntegerField(default=1, verbose_name='Использований для одного юзера')),
            ],
            options={
                'verbose_name': 'правило использований',
                'verbose_name_plural': 'правила использований',
            },
        ),
        migrations.CreateModel(
            name='ValidityRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiration_date', models.DateTimeField(verbose_name='Дата истечения')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активен?')),
            ],
            options={
                'verbose_name': 'правило валидации',
                'verbose_name_plural': 'правила валидации',
            },
        ),
        migrations.CreateModel(
            name='Ruleset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowed_users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_simple_coupons.allowedusersrule', verbose_name='Правило разрешений')),
                ('max_uses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_simple_coupons.maxusesrule', verbose_name='Правило использований')),
                ('validity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_simple_coupons.validityrule', verbose_name='Правило валидации')),
            ],
            options={
                'verbose_name': 'сет правил',
                'verbose_name_plural': 'сеты правил',
            },
        ),
        migrations.CreateModel(
            name='CouponUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times_used', models.IntegerField(default=0, editable=False, verbose_name='Кол-во использованых раз')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_simple_coupons.coupon', verbose_name='Купон')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'пользователь купона',
                'verbose_name_plural': 'пользователи купонов',
            },
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_simple_coupons.discount', verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='ruleset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_simple_coupons.ruleset', verbose_name='Сет правил'),
        ),
    ]
