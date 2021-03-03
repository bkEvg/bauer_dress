from django.db import models
from shop.models import Product, ProductSet
from django import forms
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django_simple_coupons.models import Coupon
import json


class Order(models.Model):
	paid = models.BooleanField(default=False, verbose_name='Оплачено')
	first_name = models.CharField(max_length=50, verbose_name='Имя')
	last_name = models.CharField(max_length=50, verbose_name='Фамилия')
	address = models.CharField(max_length=200, verbose_name='Адрес')
	phone = models.CharField(max_length=14, verbose_name='Тел.')
	email = models.EmailField(null=False, blank=False)
	created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
	updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
	dilivery_method = models.CharField(max_length=1, blank=False, verbose_name='Доставка')
	comment = models.CharField(max_length=200, blank=False, null=True, verbose_name='Мерки')
	coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,
	                                related_name='orders',
	                                null=True,
	                                blank=True,
	                                verbose_name='Купон')
	payment_id = models.CharField(max_length=1000, verbose_name='ID Платежа')
	

	class Meta:
		ordering = ('created',)
		verbose_name = 'заказ'
		verbose_name_plural = 'заказы'


	def __str__(self):
		return 'Order {}'.format(self.id)

	def get_total_cost(self):
	    return sum(item.get_cost() for item in self.items.all())


	def get_total(self):
		if self.coupon:
			if self.dilivery_method == '1':
				return self.coupon.get_discounted_value(self.get_total_cost())
			elif self.dilivery_method == '2':
				return self.coupon.get_discounted_value(self.get_total_cost(), 270)
			elif self.dilivery_method == '3':
				return self.coupon.get_discounted_value(self.get_total_cost())
			elif self.dilivery_method == '4':
				return self.coupon.get_discounted_value(self.get_total_cost(), 350)
			else:
				return self.coupon.get_discounted_value(self.get_total_cost())
		else:
			item_sum = sum(item.get_cost() for item in self.items.all())
			if self.dilivery_method == '1':
				return item_sum
			elif self.dilivery_method == '2':
				return item_sum + Decimal(270)
			elif self.dilivery_method == '3':
				return item_sum
			elif self.dilivery_method == '4':
				return item_sum + Decimal(350)
			else:
				return item_sum


class OrderItem(models.Model):
	
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
	product_set = models.ForeignKey(ProductSet, on_delete=models.SET_NULL, null=True, related_name='order_item_product_sets')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
	size = models.CharField(max_length=50, default="", verbose_name='Размер')
	color = models.CharField(max_length=100, default="", verbose_name='Цвет')
	
	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity
		
