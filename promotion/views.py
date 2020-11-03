from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from shop.models import Product
from .models import Promotion
from django.urls import reverse
from shop.forms import ListFilterForm
from email_sub.forms import EmailSubscription
from email_sub.models import Subscription
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse


def main(request):
	promotion = Promotion.objects.filter(is_main=True).last()
	if promotion:
		url = reverse('promo:index', kwargs={'slug': promotion.slug})
		form = EmailSubscription()
		products = Product.objects.filter(stock__gt=0, promo__promotion=promotion).order_by('-updated')
		
		return render(request, 'promotion/promo.html', {'promotion': promotion,
													'products': products,
													'url': url,
													'form': form})
	else:
		return HttpResponse('Создайте Промоушен либо проставьте статус "Главный"!')


def promo_products(request, slug):
	promotion  = get_object_or_404(Promotion, slug=slug)
	products = Product.objects.filter(stock__gt=0, promo__promotion=promotion).order_by('-updated')
	f = ListFilterForm(request.GET, queryset=products)
	paginator = Paginator(f.qs, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'shop/product/list_shop.html', {
		'products': products,
		'promotion': promotion,
		'page_obj': page_obj,
		'filter': f
	})

def promo_sort_to_expensive(request, slug=None):
	pass
	# promotion = get_object_or_404(Promotion, slug=slug)
	# products= Product.objects.filter(stock__gt=0, promo__promotion=promotion).order_by('-price')
	# f = ListFilterForm(request.GET, queryset=products)



	# paginator = Paginator(f.qs, 12)
	# page_number = request.GET.get('page')
	# page_obj = paginator.get_page(page_number)

	# return render(request, 'shop/product/list_shop.html', {
	# 	'promotion': promotion,
	# 	'products': products,
	# 	'page_obj': page_obj,
	# 	'filter': f,
	# })

def promo_sort_to_cheap(request, slug=None):
	pass
	# promotion = get_object_or_404(Promotion, slug=slug)
	# products= Product.objects.filter(stock__gt=0, promo__promotion=promotion).order_by('price')
	# f = ListFilterForm(request.GET, queryset=products)



	# paginator = Paginator(f.qs, 12)
	# page_number = request.GET.get('page')
	# page_obj = paginator.get_page(page_number)

	# return render(request, 'shop/product/list_shop.html', {
	# 	'promotion': promotion,
	# 	'products': products,
	# 	'page_obj': page_obj,
	# 	'filter': f,
	# })

@require_POST
def sub(request):
	url = request.META['HTTP_REFERER']
	if request.method == 'POST':
		form = EmailSubscription(request.POST)
		if form.is_valid():
			Subscription.objects.create(email=form.cleaned_data['email'])
			messages.success(request, message='Вы были подписаны на наши обновления! Спасибо :)')

	return redirect(url)
