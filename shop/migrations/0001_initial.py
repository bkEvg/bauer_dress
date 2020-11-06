# Generated by Django 3.1 on 2020-11-06 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seo_title', models.CharField(blank=True, max_length=250, verbose_name='SEO Название')),
                ('seo_description', models.CharField(blank=True, max_length=250, verbose_name='SEO Описание')),
                ('name', models.CharField(db_index=True, help_text='В мн.ч', max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Название (лат.)')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'цвет',
                'verbose_name_plural': 'цвета',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Материал')),
                ('description', models.CharField(max_length=250, null=True, verbose_name='Описание материала, возможно его плюсы минусы')),
                ('slug', models.SlugField(max_length=200, null=True, unique=True, verbose_name='Название (лат.)')),
            ],
            options={
                'verbose_name': 'материал',
                'verbose_name_plural': 'материалы',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Модель изделия')),
                ('description', models.CharField(max_length=250, null=True, verbose_name='Описание модели, возможно даже его преимущества')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Название (лат.)')),
            ],
            options={
                'verbose_name': 'модель изделия',
                'verbose_name_plural': 'модели изделий',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(help_text='То как этот товар будет отображен в URL.', max_length=200, verbose_name='Артикул (лат.)')),
                ('description', models.TextField(default='Full description of product', help_text='Добавьте полное описание товара, без характеристик.', null=True, verbose_name='Описание')),
                ('product_composition', models.CharField(max_length=150, null=True, verbose_name='Состав изделия')),
                ('price_from', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Цена от')),
                ('price_to', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Цена до')),
                ('stock', models.PositiveIntegerField(default=1, verbose_name='В наличии (кол-во)')),
                ('can_spend', models.BooleanField(default=False, verbose_name='Вычитать со склада')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('rent', models.BooleanField(default=False, verbose_name='Доступно в аренду (если да, заполни ниже)')),
                ('pay_method', models.CharField(blank=True, help_text='Если почасовая-ч, по дням-д, неделям-нед.', max_length=3, null=True, verbose_name='Если аренда, то какая оплата?')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.category', verbose_name='Категория')),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.material', verbose_name='Материал')),
                ('product_model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.model', verbose_name='Модель изделия')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Имя')),
                ('review', models.CharField(default='', max_length=350, verbose_name='Отзыв')),
                ('rate', models.PositiveIntegerField(default=1, verbose_name='Рейтинг')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('avatar', models.ImageField(default='default.png', upload_to='avatars/', verbose_name='Аватар')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='shop.product', verbose_name='Товар')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='SizeSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'сет размеров',
                'verbose_name_plural': 'сеты размеров',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Название (лат.)')),
            ],
            options={
                'verbose_name': 'тэг',
                'verbose_name_plural': 'тэги',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=4, null=True)),
                ('size_set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='shop.sizeset')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField(null=True, verbose_name='Ответ')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Обновлено')),
                ('review', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='shop.review', verbose_name='Отзыв')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отвечающий')),
            ],
            options={
                'verbose_name': 'ответ на отзыв',
                'verbose_name_plural': 'ответы на отзывы',
            },
        ),
        migrations.CreateModel(
            name='ProductSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='shop.product')),
                ('size_set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='size_set', to='shop.sizeset')),
            ],
            options={
                'verbose_name': 'сет товара',
                'verbose_name_plural': 'сеты товаров',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.tag', verbose_name='Тэг'),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery', verbose_name='Фото')),
                ('alt', models.CharField(max_length=30, null=True, verbose_name='Описание картинки')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
            options={
                'verbose_name': 'фото товара',
                'verbose_name_plural': 'фото товаров',
            },
        ),
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.color')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='colors', to='shop.product')),
            ],
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together={('id', 'slug')},
        ),
    ]
