from django.conf import settings 
from shop.models import Product, ProductSet
from decimal import Decimal
from django_simple_coupons.models import Coupon
from django.utils.html import format_html



class Cart(object):

	def __init__(self, request):
		"""
		Initialize cart
		"""
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		coupon_id = self.session.get(settings.COUPON_SESSION_ID)
		if not cart:
			#save na empty cart in the session
			cart = self.session[settings.CART_SESSION_ID]= {}
		self.cart = cart
		self.coupon_id = coupon_id

	def add(self, product, color, product_set_slug, quantity=1, init_price=None, update_quantity=False):
		"""
		Add product or update quantity
		"""
		product_id = str(product.id)
		price = init_price
		index = product_id + '_' + product_set_slug + str(price) + color
		if index not in self.cart:
			self.cart[index] = {
				'quantity': quantity,
				'price': str(price),
				'color': str(color),
				'product_set_slug': str(product_set_slug),
				'product_id': product.id,
			}
		elif update_quantity:
			self.cart[index]['quantity'] = quantity
		else:
			self.cart[index]['quantity'] += quantity
		self.save()


	def save(self):
		#refresh session of cart
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session[settings.COUPON_SESSION_ID] = self.coupon_id
		# mark session as modified for to be sure that session is saved
		self.session.modified = True

	def remove(self, product, price, color, quantity, product_set_slug):
		"""
		Delete a product from a cart
		"""
		product_set = ProductSet.objects.get(slug=product_set_slug)
		# size_set = product_set.size_set
		# print(size_set)
		product_id = str(product.id)
		index = product_id + '_' + product_set_slug + str(price) + color
		print(index)
		if index in self.cart:
			del self.cart[index]
			self.save()

	def __iter__(self):
		"""
		Iter objects of product and getting products from db
		"""

		for item in self.cart.values():
			item['product'] = Product.objects.get(id=item['product_id'])
			item['product_set'] = ProductSet.objects.get(slug=item['product_set_slug'])
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		"""
		Count all products in cart
		"""
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		"""
		Count price of all products in cart
		"""
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		"""
		delete cart from session
		"""
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True

	def clear_coupon(self):
		"""
		Delete a coupons from session
		"""
		del self.session[settings.COUPON_SESSION_ID]
		self.session.modified = True


	# def get_discount(self):
	#     if self.coupon:
	#         return (self.coupon.discount / Decimal('100')) * self.get_total_price()
	#     return Decimal('0')

	# def get_total_price_after_discount(self):
	#     return self.get_total_price() - self.get_discount()


	@property
	def coupon(self):
	    if self.coupon_id:
	        return Coupon.objects.get(code=self.coupon_id)
	    return None

	def get_discount(self):
	    if self.coupon:
	        return self.coupon.get_discount 
	    return Decimal('0')

	def get_total_price_after_discount(self):
		if self.coupon:
			return self.coupon.get_discounted_value(self.get_total_price())
		return self.get_total_price()


	def get_discounted_value(self): #how much price was discounted
		return self.get_total_price() - self.get_total_price_after_discount()