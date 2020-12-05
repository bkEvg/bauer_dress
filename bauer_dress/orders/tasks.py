from django.core.mail import send_mail
from .models import Order
from bauer_dress.celery import app
from django.shortcuts import render
from shop.models import Product
from django.template import loader
from cart.cart import Cart
from django.conf import settings

@app.task(bind=True, default_retry_delay=5*60)
def order_created(self, order_id):
	"""
	Task for sending mail if order created
	"""
	order = Order.objects.get(id=order_id)
	subject = 'Заказ #{}'.format(order.id)
	html = loader.render_to_string('orders/order/mail2.html', context={
		'order': order})
	order_sent = send_mail(subject, None, settings.EMAIL_HOST_USER, [order.email, settings.MAIL], html_message=html)
	try:
		return order_sent
	except Exception as exp:
		raise self.retry(exc=exc, countdown=60)