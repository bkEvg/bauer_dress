from django.contrib import admin
from .models import Wishlist, WishlistItem

class WishlistItemInline(admin.TabularInline):
	model = WishlistItem
	fk_name = 'wishlist'


class WishlistAdmin(admin.ModelAdmin):
	list_display=['user']
	inlines = [WishlistItemInline,]
admin.site.register(Wishlist, WishlistAdmin)