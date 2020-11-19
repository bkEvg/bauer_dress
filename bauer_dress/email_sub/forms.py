from django import forms
from .models import Subscription

class EmailSubscription(forms.ModelForm):
	class Meta:
		model = Subscription
		fields = ['email']