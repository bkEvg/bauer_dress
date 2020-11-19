from django import forms
from .models import WishlistItem
from shop.models import Color, Size



colors = [('{}'.format(color.name), '{}'.format(color.name)) for color in Color.objects.all()]

class WishlistAddProductForm(forms.Form):
	quantity = forms.IntegerField()
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
	color = forms.TypedChoiceField(choices=colors)