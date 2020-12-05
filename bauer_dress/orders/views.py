from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
from shop.models import Product
from django.contrib.admin.views.decorators import staff_member_required
from django_simple_coupons.forms import CouponApplyForm
import weasyprint
from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from email_sub.models import Subscription
from django.core.exceptions import ObjectDoesNotExist
from .tasks import order_created


def order_create(request):
	cart = Cart(request)
	coupon_apply_form = CouponApplyForm()
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save(commit=False)
			if cart.coupon:
			    order.coupon = cart.coupon
			    order.discount = cart.coupon.discount.value
			order.save()
			for item in cart:
				OrderItem.objects.create(order=order,
										product=item['product'],
										product_set=item['product_set'],
										price=item['product_set'].price,
										quantity=item['quantity'],
										size = item['product_set'].size_set,
										color = item['color'])
			try:
				Subscription.objects.get(email=order.email)
			except ObjectDoesNotExist:
				Subscription.objects.create(name=order.first_name, surname=order.last_name, email=order.email)
			# send email with html template
			# subject = 'Заказ #{}'.format(order.id)
			# html = loader.render_to_string('orders/order/mail2.html', context={
			# 	'order': order,
			# 	'cart': cart})
			# mail_sent = send_mail(subject, None, settings.EMAIL_HOST_USER, [order.email, settings.MAIL], html_message=html)
			#clearing cart and coupon
			order_created.delay(order.id)
			cart.clear()
			if cart.coupon:
				cart.clear_coupon()
			return render(request, 'orders/order/created.html', {'order': order})
	else:
		form = OrderCreateForm()
	return render(request, 'orders/order/create_v2.html', {'cart': cart,
														'form': form,
														'coupon_apply_form': coupon_apply_form})

@staff_member_required
def admin_order_detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	coupon = order.coupon
	
	return render(request, 'admin/orders/order/detail.html', {'order': order})



@staff_member_required
def admin_order_pdf(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	html = loader.render_to_string('orders/order/pdf.html', {'order': order})
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename=\
									"order_{}.pdf"'.format(order.id)
	weasyprint.HTML(
		string=html
		).write_pdf(response,
			stylesheets=[weasyprint.CSS(str(settings.STATIC_ROOT) + '/css/pdf.css')])
	return response 




