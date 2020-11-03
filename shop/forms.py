from django import forms
from .models import Review, Product, Category, ReviewResponse
import django_filters
from django.db import models


class ReviewForm(forms.Form):
	class Meta:
		model = Review
		fields = ['name', 'review', 'rate']




# class PriceFilterForm(django_filters.FilterSet):
#     sort_by_price = django_filters.CharFilter(field_name='price', method='filter_price')

#     def filter_price(self, queryset, name, value):
#         return queryset.filter(stock__gt=0).order_by('-price')


class ListFilterForm(django_filters.FilterSet):
    rent = django_filters.BooleanFilter(field_name='rent', widget=forms.CheckboxInput)

    class Meta:
        model = Product
        fields = {
            'price_from': ['lt'],
            'price_to': ['gt'],
            # 'rent': ['exact'],
            'product_model': ['exact'],
            'material': ['exact'],
            'tag': ['exact'],
            'category': ['exact']
        }


class ForRentFilterForm(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'price_from': ['lt'],
            'price_to': ['gt'],
            'product_model': ['exact'],
            'material': ['exact'],
            'tag': ['exact'],
            'category': ['exact']
        }


class ReviewResponseForm(forms.ModelForm):
    class Meta:
        model = ReviewResponse
        fields = ['response']