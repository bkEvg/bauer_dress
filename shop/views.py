from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Category, Product, Review, Material, Tag, ReviewForm, Size, \
	Tag, ProductSet, SizeSet, ReviewResponse
from django.utils import timezone
from cart.forms import CartAddProductForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import ListFilterForm, ReviewResponseForm, ForRentFilterForm
from promotion.models import Promotion
from django.core.exceptions import ObjectDoesNotExist
from allauth.account.decorators import verified_email_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST



def product_detail(request, id, slug, category_slug):
	product = get_object_or_404(Product, id=id, slug=slug, stock__gt=0)
	cart_product_form = CartAddProductForm()
	review_form = ReviewForm()
	response_form = ReviewResponseForm()
	category = get_object_or_404(Category, slug=category_slug)
	products_with_category_exclude = Product.objects.filter(category=category, stock__gte=1).exclude(id=product.id)[:4]
	if products_with_category_exclude.count() <= 1:
		products_with_category_exclude = None
	
	
	return render(request, 'shop/distribution/detail.html', {'product': product,
														'cart_product_form': cart_product_form,
														'review_form': review_form,
														'response_form': response_form,
														'category': category,
														'category_products': products_with_category_exclude})



def product_set__detail(request, id, slug, category_slug, set_slug):
	product = get_object_or_404(Product, id=id, slug=slug, stock__gt=0)
	cart_product_form = CartAddProductForm()
	review_form = ReviewForm()
	response_form = ReviewResponseForm()
	category = get_object_or_404(Category, slug=category_slug)
	products_with_category_exclude = Product.objects.filter(category=category, stock__gte=1).exclude(id=product.id)[:5]
	if products_with_category_exclude.count() <= 1:
		products_with_category_exclude = None
	set = get_object_or_404(ProductSet, slug=set_slug)
	size_set = get_object_or_404(SizeSet, size_set=set)
	sets = product.sets.all().exclude(size_set=size_set)
	current_set = product.sets.get(size_set=size_set)



	return render(request, 'shop/distribution/detail_with_set.html', {'product': product,
														'cart_product_form': cart_product_form,
														'review_form': review_form,
														'response_form': response_form,
														'category': category,
														'set': set,
														'sets': sets,
														'current_set': current_set,
														'category_products': products_with_category_exclude})




def product_list(request, category_slug=None, tag_slug=None):
	category = None
	tag = None
	categories = Category.objects.all()
	products = Product.objects.filter(stock__gt=0).order_by('-updated')
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = Product.objects.filter(stock__gt=0, category=category)

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		products = Product.objects.filter(stock__gt=0, tag=tag)
	f = ListFilterForm(request.GET, queryset=products)



	paginator = Paginator(f.qs, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	

	return render(request, 'shop/product/list_shop.html', {
		'page_obj': page_obj,
		'filter': f,
		'category':category,
		'tag': tag,
	})

def for_rent(request):
	products = Product.objects.filter(stock__gt=0, rent=True).order_by('-updated')
	f = ForRentFilterForm(request.GET, queryset=products)

	paginator = Paginator(f.qs, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'shop/product/for_rent_list.html', {
		'page_obj': page_obj,
		'filter': f,
	})


@verified_email_required
def rate_product(request, id):
	product = get_object_or_404(Product, id=id)
	url = product.get_absolute_url()
	form = ReviewForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		if cd['rating']:
			review = Review.objects.create(user=request.user, product=product, name=cd['name'], review=cd['review'], rate=cd['rating'])
		else:
			review = Review.objects.create(user=request.user, product=product, name=cd['name'], review=cd['review'], rate=0)
		review.save()
		messages.success(request, message='Ваш отзыв опубликован. Спасибо!')
	return redirect(url)



def error404(request, *args, **kwargs):
	return render(request, 'shop/404.html')

def error500(request, *args, **kwargs):
	return render(request, 'shop/500.html')


def cheap_product_list(request):
	# promotion = None
	products = Product.objects.filter(stock__gt=0).order_by('price')
	# if slug:
	# 	promotion = get_object_or_404(Promotion, slug=slug)
	# 	products= Product.objects.filter(stock__gt=0, promo__promotion=promotion).order_by('price')
	f = ListFilterForm(request.GET, queryset=products)



	paginator = Paginator(f.qs, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)


	return render(request, 'shop/product/list_shop.html', {
		'products': products,
		'page_obj': page_obj,
		'filter': f,
	})



def expensive_product_list(request):
	# promotion = None
	products = Product.objects.filter(stock__gt=0).order_by('-price')
	# if slug:
	# 	promotion = get_object_or_404(Promotion, slug=slug)
	# 	products= Product.objects.filter(stock__gt=0, promo__promotion=promotion).order_by('-price')
	f = ListFilterForm(request.GET, queryset=products)



	paginator = Paginator(f.qs, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	return render(request, 'shop/product/list_shop.html', {
		'products': products,
		'page_obj': page_obj,
		'filter': f,
	})




def new_products(request):
	products = []
	product_list = Product.objects.filter(stock__gt=0)
	for product in product_list:
		if product.status_new():
			products.append(product)
		else:
			continue
	
	return render(request, 'shop/product/list_shop.html', {
		'products': products,
	})

def main(request):
	return render(request, 'shop/main.html')


@staff_member_required
def review_response(request, review_id):
	review = Review.objects.get(pk=review_id)
	url = request.META['HTTP_REFERER']
	if request.method == 'POST':
		form = ReviewResponseForm(request.POST)
		if form.is_valid():
			ReviewResponse.objects.create(user=request.user, review=review, response=form.cleaned_data['response'])
	messages.success(request, message='Ответ опубликован!')
	return redirect(url)