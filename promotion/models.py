from django.db import models
from shop.models import Product, Category
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class SeoPromotion(models.Model):
	seo_title = models.CharField('SEO Название', blank=True, max_length=250)
	seo_description = models.CharField('SEO Описание', blank=True, max_length=250)

	def get_seo_title(self):
		if self.seo_title:
			return self.seo_title
		else:
			return ''

	def get_seo_description(self):
		if self.seo_description:
			return self.seo_description
		else:
			return ''


	class Meta:
		abstract = True

class FirstPage(models.Model):
	name = models.CharField('Название для этого тэмплейта', max_length=100, blank=True)
	button = models.CharField('Надпись на кнопке', max_length=70, blank=False, null=True,
		help_text='Максимум 2 слова с предлогом, побуждение что-то сделать, например: узнать, перейти и тд')
	image = models.ImageField(upload_to='promo/first_page/images', verbose_name='Главное фото',
		help_text='Примерные размеры фото 1900х650, сам товар находится в правой части фото,\
		если разделить фото на три части двумя линиями, то товар на второй линии')


	class Meta:
		verbose_name = 'Главная страница'
		verbose_name_plural = '1. Главные страницы'

	def __str__(self):
		return self.name



class SecondPage(models.Model):
	name = models.CharField('Название для этого тэмплейта', max_length=100, blank=True)

	subtitle = models.CharField('Подзаголовок страницы', max_length=200, blank=True, null=True)
	title = models.CharField('Заголовок страницы', max_length=200, blank=True, null=True)

	first_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_no_1')
	image_for_first_cat = models.ImageField(upload_to='promo/second_page/first_category/images', verbose_name='Фото категории', 
		help_text='Левая колонка 750x1050')
	alt_for_image_no_1 = models.CharField('Описание картинки 1', max_length=100, blank=False, null=True)


	second_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_no_2')
	image_for_second_cat = models.ImageField(upload_to='promo/second_page/second_category/images', verbose_name='Фото категории',
		help_text='Центральная колонка, верх 750x500')
	alt_for_image_no_2 = models.CharField('Описание картинки 2', max_length=100, blank=False, null=True)


	third_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_no_3')
	image_for_third_cat = models.ImageField(upload_to='promo/second_page/third_category/images', verbose_name='Фото категории',
		help_text='Центральная колонка, низ 750x500')
	alt_for_image_no_3 = models.CharField('Описание картинки 3', max_length=100, blank=False, null=True)



	fourth_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_no_4')
	image_for_fourth_cat = models.ImageField(upload_to='promo/second_page/fourth_category/images', verbose_name='Фото категории', 
		help_text='Правая колонка 750x1050')
	alt_for_image_no_4 = models.CharField('Описание картинки 4', max_length=100, blank=False, null=True)



	class Meta:
		verbose_name = 'Вторая страница'
		verbose_name_plural = '2. Вторые страницы'


	def __str__(self):
		return self.name



class ThirdPage(models.Model):
	name = models.CharField('Название для этого тэмплейта', max_length=100, blank=True)


	subtitle = models.CharField('Подзаголовок страницы', max_length=200, blank=True, null=True)
	title = models.CharField('Заголовок страницы', max_length=200, blank=True, null=True)


	class Meta:
		verbose_name = 'Третья страница'
		verbose_name_plural = '3. Третьи страницы'


	def __str__(self):
		return self.name


class ServicePage(models.Model):
	name = models.CharField('Название для этого тэмплейта', max_length=100, blank=True)


	title_1 = models.CharField('Заголовок первой услуги', max_length=40, blank=True, null=True)
	subtitle_1 = models.CharField('Подзаголовок первой услуги', max_length=40, blank=True, null=True)
	
	title_2 = models.CharField('Заголовок второй услуги', max_length=40, blank=True, null=True)
	subtitle_2 = models.CharField('Подзаголовок второй услуги', max_length=40, blank=True, null=True)
	
	title_3 = models.CharField('Заголовок третьей услуги', max_length=40, blank=True, null=True)
	subtitle_3 = models.CharField('Подзаголовок третьей услуги', max_length=40, blank=True, null=True)


	class Meta:
		verbose_name = 'Четвертая страница'
		verbose_name_plural = '4. Страницы услуг'


	def __str__(self):
		return self.name


class SubPage(models.Model):
	name = models.CharField('Название для этого тэмплейта', max_length=100, blank=True)


	title = models.CharField('Заголовок страницы', max_length=200, blank=True, null=True)
	subtitle = models.CharField('Подзаголовок страницы', max_length=200, blank=True, null=True)


	class Meta:
		verbose_name = 'Пятая страница'
		verbose_name_plural = '5. Пятые страницы'


	def __str__(self):
		return self.name



# class TopProducts(models.Model):
# 	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
# 	page = models.ForeignKey(ThirdPage, on_delete=models.CASCADE, related_name='products')



class Promotion(SeoPromotion):
	theme_of_promo = models.CharField('Тема акции \n(подзаголовок на главной)', max_length=60)
	offer = models.CharField('Оффер на главной странице', max_length=100, blank=False)
	slug = models.SlugField(max_length=200, unique=True, blank=False, null=True)
	first_page = models.ForeignKey(FirstPage, verbose_name='Первый экран', on_delete=models.SET_NULL, null=True)
	second_page = models.ForeignKey(SecondPage, verbose_name="Второй экран", on_delete=models.SET_NULL, null=True)
	third_page = models.ForeignKey(ThirdPage, verbose_name="Третий эран", on_delete=models.SET_NULL, null=True)
	service_page = models.ForeignKey(ServicePage, verbose_name='Экран услуг', on_delete=models.SET_NULL, null=True, related_name='service')
	sub_page = models.ForeignKey(SubPage, verbose_name='Экран подписки', on_delete=models.SET_NULL, null=True)
	is_main = models.BooleanField('Главный', default=False)

	def get_absolute_url(self):
		return reverse('promo:exact_promo', kwargs={'slug': self.slug})

	def __str__(self):
		return self.theme_of_promo

	class Meta:
		verbose_name='промоушн'
		verbose_name_plural='промоушны'


class PromoProduct(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promo')
	promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='products')


	class Meta:
		verbose_name='промо товар'
		verbose_name_plural='промо товары'