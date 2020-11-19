from django.core.mail import send_mail
from .models import Order
# from myshop.celery import app
from django.shortcuts import render
from shop.models import Product


from asgiref.sync import sync_to_async


# @app.task
def order_created(request, order_id):
	"""
	Task for sending mail if order created
	"""
	order = Order.objects.get(id=order_id)
	subject = 'Заказ №{}'.format(order_id)
	message = 'Дорогой {},\n\nЗаказ успешно оформлен.\
				Номер Вашего заказа: {}'.format(order.first_name, order.id)
	html = render(request, 'orders/order/mail.html', {'order': order})
	mail_sent = send_mail(subject, message, 'bk.evg@mail.ru', [order.email], html_message=html)
	return mail_sent

