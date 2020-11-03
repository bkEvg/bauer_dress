from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from shop.models import Color, SizeSet, ProductSet

class Wishlist(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name='лист желаний'
		verbose_name_plural='лист желаний'


class WishlistItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='товар')
	wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
	# size_set = models.ForeignKey(SizeSet, on_delete=models.SET_NULL, null=True, related_name='wish_size_set')
	product_set = models.ForeignKey(ProductSet, on_delete=models.SET_NULL, null=True, related_name='product_set')
	date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
	quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
	status_bought = models.BooleanField("Добавлен в корзину", default=False)

	class Meta:
		verbose_name='желание'
		verbose_name_plural='желания'

	def get_cost(self):
		return self.price * self.quantity

