from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart 
from .forms import CartAddProductForm
from shop.models import Product, ProductSet
from django.views.decorators.http import require_POST
from django.contrib import messages
from django_simple_coupons.forms import CouponApplyForm
from wishlist.models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist


@require_POST
def cart_add(request, product_id, price, product_set_slug):
	cart = Cart(request)
	url = request.META['HTTP_REFERER']
	product = get_object_or_404(Product, id=product_id)
	product_set = get_object_or_404(ProductSet, slug=product_set_slug)
		
	#mark product in wishlist as bought
	try:
		wishlist = Wishlist.objects.get(user=request.user)
	except:
		wishlist = None
		wishlist_item = None
	if wishlist:
		try:
			wishlist_item = wishlist.items.get(product=product, price=price, product_set=product_set)
			wishlist_item.status_bought = True
			wishlist_item.save()
		except ObjectDoesNotExist:
			wishlist_item = None

	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		if wishlist_item:
			cart.add(product=product, quantity=cd['quantity'], init_price=wishlist_item.price, product_set_slug=product_set.slug, color=cd['color'], update_quantity=cd['update'])
		else:
			cart.add(product=product, quantity=cd['quantity'], init_price=price, product_set_slug=product_set.slug, color=cd['color'], update_quantity=cd['update'])
		messages.success(request, message='Товар добавлен в Корзину!')
	return redirect(url)

def cart_remove(request, product_id, price, color, quantity, product_set_slug):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	product_set = get_object_or_404(ProductSet, slug=product_set_slug)

	try:
		wishlist = Wishlist.objects.get(user=request.user)
	except:
		wishlist = None

	cart.remove(product, price, color, quantity, product_set_slug)

	#mark product in wishlist as non bought
	if wishlist:
		try:
			wishlist_item = wishlist.items.get(product=product, price=price, product_set=product_set, quantity=quantity)
			wishlist_item.status_bought = False
			wishlist_item.save()
		except ObjectDoesNotExist:
			wishlist_item = None

	messages.success(request, message='Товар удален из Корзины!')
	return redirect('cart:cart_detail')


def cart_detail(request):
	cart = Cart(request)
	coupon_apply_form = CouponApplyForm()
	return render(request, 'cart/detail.html', {'cart': cart,
						'coupon_apply_form': coupon_apply_form})

def cart_clear(request):
	cart = Cart(request)
	cart.clear()
	cart.clear_coupon()
	return redirect('cart:cart_detail')

def cart_clear_coupon(request):
	cart = Cart(request)
	cart.clear_coupon()
	return redirect('cart:cart_detail')