from django.contrib import admin
from .models import Subscription

class SubscriptioAdmin(admin.ModelAdmin):
	list_display = ['email','name', 'surname', 'date_sub']
admin.site.register(Subscription, SubscriptioAdmin)

