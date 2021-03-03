from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
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
from notifications.signals import notify
from django.contrib.auth.models import Group
from decimal import Decimal
from yookassa import Payment
import uuid
from django.urls import reverse


def bad_results(request):
	return render(request, 'orders/order/created_bad.html')

def finish(request):
	return render(request, 'orders/order/created.html')

def thank_you(request, order_id):
	cart = Cart(request)
	order = Order.objects.get(pk=order_id)
	payment = Payment.find_one(order.payment_id)
	if payment.paid == True:
		idempotence_key = str(uuid.uuid4())
		response = Payment.capture(
		  order.payment_id,
		  {
		    "amount": {
		      "value": Decimal(order.get_total()),
		      "currency": "RUB"
		    }
		  },
		  idempotence_key
		)
		order.paid = True
		for item in order.items.all():
			if item.product.can_spend:
				if item.product.stock >= item.quantity:
					item.product.stock -= item.quantity
					item.product.save()
				else:
					pass
			else:
				pass
		order.save()
		cart.clear()
		if cart.coupon:
			cart.clear_coupon()
		return redirect('orders:finish')
	else:
		return redirect('orders:bad_results')



def order_create(request):
	cart = Cart(request)
	user = request.user
	admins = Group.objects.get(name='staff')
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
										price=item['price'],
										quantity=item['quantity'],
										size = item['product_set'].size_set,
										color = item['color'])
			try:
				Subscription.objects.get(email=order.email)
			except ObjectDoesNotExist:
				Subscription.objects.create(name=order.first_name, surname=order.last_name, email=order.email)
			###

			idempotence_key = str(uuid.uuid4())
			payment = Payment.create({
			    "amount": {
			      "value": str(order.get_total()),
			      "currency": "RUB"
			    },
			    "payment_method_data": {
			      "type": "bank_card"
			    },
			    "confirmation": {
			      "type": "redirect",
			      "return_url": "https://b6dc82179c04.ngrok.io{}".format(reverse('orders:thank_you', args=[order.id]))
			    },
			    "description": "Заказ №%s" % order.id
			}, idempotence_key)
			order.payment_id = payment.id
			order.save()

			# get confirmation url
			confirmation_url = payment.confirmation.confirmation_url
			####

			#clearing cart and coupon
			notify.send(admins, recipient=admins, action_object=order, verb=f'Заказ #{order.id}')
			order_created.delay(order.id)
			return redirect(confirmation_url)
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




