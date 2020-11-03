from django import forms
from .models import Order
from phonenumber_field.formfields import PhoneNumberField

#

class OrderCreateForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'dilivery_method']
