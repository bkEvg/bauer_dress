from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone
from django.utils import timezone
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from decimal import Decimal


class SeoModel(models.Model):
    seo_title = models.CharField('SEO Название', blank=True, max_length=250)
    seo_description = models.CharField('SEO Описание', blank=True, max_length=250)

    def get_seo_title(self):
        if self.seo_title:
            return self.seo_title
        return ''

    def get_seo_description(self):
        if self.seo_description:
            return self.seo_description
        return ''

    class Meta:
        abstract = True


class Category(SeoModel):
	"""
	Product's category model
	"""
	name = models.CharField(max_length=200, db_index=True, verbose_name=u"Название",
		help_text='В мн.ч')
	slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name=u"Название (лат.)")


	class Meta:
		ordering=('name',)
		verbose_name = 'категория'
		verbose_name_plural = 'категории'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:index_by_category', args=[self.slug])


class Material(models.Model):
	name = models.CharField('Материал', max_length=50)
	description = models.CharField('Описание материала, возможно его плюсы минусы', max_length=250, blank=False, null=True)
	slug = models.SlugField(max_length=200, unique=True, null=True, verbose_name=u"Название (лат.)")



	def __str__(self):
		return self.name

	class Meta:
		verbose_name='материал'
		verbose_name_plural = 'материалы'

	def get_absolute_url(self):
		return reverse('shop:index_by_material', kwargs={'material_slug': self.slug})


class Model(models.Model):
	name = models.CharField(max_length=50, blank=False, verbose_name='Модель изделия')
	description = models.CharField('Описание модели, возможно даже его преимущества', max_length=250, blank=False, null=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name=u"Название (лат.)")


	def __str__(self):
		return self.name

	class Meta:
		verbose_name='модель изделия'
		verbose_name_plural = 'модели изделий'

	def get_absolute_url(self):
		return reverse('shop:index_by_model', args=[self.slug])


class Tag(models.Model):
	name = models.CharField(max_length=50, blank=False, verbose_name='Название')
	slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name=u"Название (лат.)")

	class Meta:
		verbose_name = 'тэг'
		verbose_name_plural = 'тэги' 

	def __str__(self):
		return self.name	


	def get_absolute_url(self):
		return reverse('shop:index_by_tag', kwargs={'tag_slug': self.slug})



class Product(models.Model):
	"""
	Product model
	"""
	category = models.ForeignKey(Category, related_name='products', 
		on_delete=models.SET_NULL, null=True, verbose_name=u"Категория")
	name = models.CharField(max_length=200, db_index=True, verbose_name=u"Название")
	slug = models.SlugField(max_length=200, db_index=True, verbose_name=u"Артикул (лат.)", 
		help_text='То как этот товар будет отображен в URL.')
	description = models.TextField(default='Full description of product',blank=False, null=True, verbose_name=u"Описание",
		help_text='Добавьте полное описание товара, без характеристик.')
	short_description = models.CharField(default='Short description of product', max_length=100, verbose_name=u"Краткое описание", blank=False, null=True,
		help_text='Краткое описание, 3-4 слова.')
	product_model = models.ForeignKey(Model, on_delete=models.CASCADE, null=True, verbose_name='Модель изделия')
	product_composition = models.CharField(max_length=150, blank=False, null=True, verbose_name='Состав изделия')
	material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, verbose_name=u"Материал")
	price_from = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"Цена от", blank=False, null=True)
	price_to = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u"Цена до", blank=False, null=True)
	stock = models.PositiveIntegerField(default=1, verbose_name=u"В наличии (кол-во)")
	can_spend = models.BooleanField(default=False, verbose_name=u"Вычитать со склада")
	created = models.DateTimeField(auto_now_add=True, verbose_name=u"Создан")
	updated = models.DateTimeField(auto_now=True, verbose_name=u"Обновлен")
	tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, verbose_name='Тэг')
	rent = models.BooleanField("Доступно в аренду (если да, заполни ниже)", default=False)
	pay_method = models.CharField("Если аренда, то какая оплата?", blank=True, null=True, max_length=3, help_text='Если почасовая-ч, по дням-д, неделям-нед.')
	# discount = models.IntegerField(default=0, blank=True,
 #                                    validators=[MinValueValidator(0),
 #                                                MaxValueValidator(100)],
 #                                                verbose_name='Скидка (%)')
	
	def __str__(self):
		return self.name

	class Meta:
		index_together = (('id','slug'),)
		verbose_name = 'товар'
		verbose_name_plural = 'товары'

	# def get_price(self):
	#     return Decimal(self.price - self.price * (self.discount / Decimal('100')))


	def status_new(self):
		now = timezone.now()
		if now + datetime.timedelta(days=-5) < self.created < now:
			return True
		else:
			return False


	def get_absolute_url(self):
		return reverse('shop:details', args=[self.category.slug, self.id, self.slug])


	def get_review_count(self):
		review_count = 0
		for review in self.reviews.all():
			review_count += 1
		return review_count

	def get_rating_tag(self):
		rating_sum = 0 #collect all ratings and after all i will divide it
		reviews_counter = 0
		average_rating_tag = 'zero'
		if self.reviews.all():
			for review in self.reviews.all():
				reviews_counter += 1
				rating_sum += review.rate
			average_rating = int(rating_sum / reviews_counter)
			if average_rating == 0:
				average_rating_tag = 'zero'
			if average_rating == 1:
				average_rating_tag = 'one'
			if average_rating == 2:
				average_rating_tag = 'two'
			if average_rating == 3:
				average_rating_tag = 'three'
			if average_rating == 4:
				average_rating_tag = 'four'
			if average_rating == 5:
				average_rating_tag = 'five'
			return average_rating_tag
		return average_rating_tag




class Gallery(models.Model):
    """
    Model for Product which allow to add much photos
    """

    image = models.ImageField(upload_to='gallery', verbose_name='Фото')
    alt = models.CharField('Описание картинки', max_length=30, blank=False, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
    	verbose_name = 'фото товара'
    	verbose_name_plural = 'фото товаров'



class SizeSet(models.Model):

	def __str__(self):
		return '{0}-{1}'.format(self.sizes.filter().first(), self.sizes.filter().last())


class Size(models.Model):
	size = models.CharField(max_length=4, null=True)
	size_set = models.ForeignKey(SizeSet, on_delete=models.CASCADE, null=True, related_name='sizes')

	def __str__(self):
		return self.size



class Color(models.Model):
	name = models.CharField('Цвет', default='', max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'цвет'
		verbose_name_plural = 'цвета'

class Colors(models.Model):
	color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='colors')



class ProductSet(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sets')
	size_set = models.ForeignKey(SizeSet, on_delete=models.SET_NULL, null=True, related_name='size_set')
	price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, verbose_name=u"Цена")
	slug = models.SlugField(max_length=200, unique=True, db_index=True)

	class Meta:
		verbose_name = 'сет товара'
		verbose_name_plural = 'сеты товаров'

	def __str__(self):
		return 'Сет {0} {1} {2}'.format(self.product.name, self.size_set, self.price)


	def get_absolute_url(self):
		return reverse('shop:product_set__detail', args=[self.product.category.slug, self.product.id, self.product.slug, self.slug])



class Review(models.Model):
	"""
	Review models
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
	name = models.CharField(max_length=30, blank=False, verbose_name='Имя')
	review = models.CharField(max_length=350, default='', blank=False, null=False, verbose_name='Отзыв')
	rate = models.PositiveIntegerField(default=1, blank=False, null=False, verbose_name='Рейтинг')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
	updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
	avatar = models.ImageField(default='default.png', upload_to='avatars/', verbose_name='Аватар')

	# def get_queryset(self):
	# 	return self.product.reviews.all()[:5]

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'отзыв'
		verbose_name_plural = 'отзывы'
		ordering = ('-created',)

	def get_review_rate_tag(self):
		rating_tag = 'zero'
		if self.rate == 0:
			rating_tag = 'zero'
		if self.rate == 1:
			rating_tag = 'one'
		if self.rate == 2:
			rating_tag = 'two'
		if self.rate == 3:
			rating_tag = 'three'
		if self.rate == 4:
			rating_tag = 'four'
		if self.rate == 5:
			rating_tag = 'five'
		return rating_tag


class ReviewResponse(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, verbose_name='Отзыв', related_name='responses')
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Отвечающий')
	response = models.TextField(blank=False, null=True, verbose_name='Ответ')
	created = models.DateTimeField(auto_now_add=True, blank=False, null=True, verbose_name='Создано')
	updated = models.DateTimeField(auto_now=True, blank=False, null=True, verbose_name='Обновлено')

	def __str__(self):
		return 'ответ для {}'.format(self.review.name)

	class Meta:
		verbose_name = 'ответ на отзыв'
		verbose_name_plural = 'ответы на отзывы'


class ReviewForm(ModelForm):
	"""
	Form for reviews
	"""
	ratings = [(i , str(i)) for i in range(1, 6)]
	rating = forms.TypedChoiceField(choices=ratings, coerce=int, widget=forms.RadioSelect())
	class Meta:
		model = Review
		fields = ['name', 'review']
		widgets = {
            'review': forms.Textarea(),
        }

