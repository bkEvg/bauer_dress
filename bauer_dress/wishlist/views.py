from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
# from .forms import WishlistForm
from cart.forms import CartAddProductForm
from allauth.account.decorators import verified_email_required

from shop.models import SizeSet, ProductSet, Product
from cart.cart import Cart

@verified_email_required
def index(request):
	try:
		wishlist = Wishlist.objects.get(user=request.user)
	except ObjectDoesNotExist:
		wishlist = Wishlist.objects.create(user=request.user)
	cart_product_form = CartAddProductForm()
	return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist,
				'cart_product_form': cart_product_form})



@verified_email_required
def wishlist_add(request, product_id, price, product_set_slug):

	wishlist = Wishlist.objects.get(user=request.user)
	product_set = get_object_or_404(ProductSet, slug=product_set_slug)
	# size_set = get_object_or_404(SizeSet, size_set=set)
	product = get_object_or_404(Product, id=product_id)
	url = request.META.get('HTTP_REFERER')
	wishlist_items = None
	try:
		wishlist_items = wishlist.items.get(product=product, price=price, product_set=product_set)
	except ObjectDoesNotExist:
		pass

	if wishlist_items in wishlist.items.all():
		wishlist_items = wishlist.items.get(product=product, price=price, product_set=product_set)
		wishlist_items.quantity +=1
		wishlist_items.save()
	else:
		wishlist_items = wishlist.items.create(product=product, price=price, product_set=product_set)
	messages.success(request, message='Товар успешно добавлен в Желания!')
	return redirect(url)

def wishlist_remove(request, product_id, price, quantity, product_set_slug):
	url = request.META.get('HTTP_REFERER')
	product_set = get_object_or_404(ProductSet, slug=product_set_slug)
	# size_set = get_object_or_404(SizeSet, size_set=set)
	wishlist = Wishlist.objects.get(user=request.user)
	product = get_object_or_404(Product, id=product_id)
	wishlist_items = wishlist.items.get(product=product, price=price, product_set=product_set, quantity=quantity).delete()
	messages.success(request, message='Товар успешно удален из Желаний!')
	return redirect(url)



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