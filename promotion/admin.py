from django.contrib import admin
from .models import Promotion, PromoProduct, FirstPage, SecondPage, \
	ThirdPage, TopProducts, ServicePage, SubPage


class PromoProductInline(admin.TabularInline):
	fk_name = 'promotion'
	model = PromoProduct


class PromotionAdmin(admin.ModelAdmin):
	list_display = ['theme_of_promo', 'offer']
	search_fields = ['theme_of_promo', 'offer']
	prepopulated_fields = {'slug': ('offer',)}
	inlines = [PromoProductInline,]
admin.site.register(Promotion, PromotionAdmin)


class FirstPageAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']
admin.site.register(FirstPage, FirstPageAdmin)


class SecondPageAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']
admin.site.register(SecondPage, SecondPageAdmin)


class ServicePageAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']
admin.site.register(ServicePage, ServicePageAdmin)


class SubPageAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']
admin.site.register(SubPage, SubPageAdmin)


class ThirdPageInline(admin.TabularInline):
	fk_name = 'page'
	model = TopProducts


class ThirdPageAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']
	inlines = [ThirdPageInline]
admin.site.register(ThirdPage, ThirdPageAdmin)