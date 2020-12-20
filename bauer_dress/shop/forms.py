from django import forms
from .models import Review, Product, Category, ReviewResponse
import django_filters
from django.db import models


class ReviewForm(forms.Form):
	class Meta:
		model = Review
		fields = ['name', 'review', 'rate']



class ListFilterForm(django_filters.FilterSet):
    rent = django_filters.BooleanFilter(field_name='rent', widget=forms.CheckboxInput)

    class Meta:
        model = Product
        fields = {
            'price_from': ['lt'],
            'price_to': ['gt'],
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
            'material': ['exact'],
            'tag': ['exact'],
            'category': ['exact']
        }


class ReviewResponseForm(forms.ModelForm):
    class Meta:
        model = ReviewResponse
        fields = ['response']


