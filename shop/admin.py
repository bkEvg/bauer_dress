from django.contrib import admin
from .models import Category, Product, Gallery, Review, Material, \
	Tag, Model, Color, Colors, ReviewResponse, ProductSet, SizeSet, Size


class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name',]
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery


class ColorsInline(admin.TabularInline):
    fk_name = 'product'
    model = Colors


class TagAdmin(admin.ModelAdmin):
	list_display = ['name']
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Tag, TagAdmin)


class ColorAdmin(admin.ModelAdmin):
	list_display = ['name']
admin.site.register(Color, ColorAdmin)



class MaterialAdmin(admin.ModelAdmin):
	list_display=['name',]
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Material, MaterialAdmin)
		
class ModelAdmin(admin.ModelAdmin):
	list_display=['name',]
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Model, ModelAdmin)
		

class ProductSetInline(admin.TabularInline):
	prepopulated_fields = {'slug': ('size_set', 'price',)}
	model = ProductSet
	fk_name = 'product'


class ProductAdmin(admin.ModelAdmin):
	list_display = ['name','stock', 'updated', 'price_from', 'price_to']
	list_filter = ['created', 'updated',]
	list_editable = ['stock',]
	prepopulated_fields = {'slug': ('name',)}
	inlines = [ProductSetInline, GalleryInline]
	ordering = ('updated',)
	search_fields = ['name', 'slug']
admin.site.register(Product, ProductAdmin,)


class ReviewAdmin(admin.ModelAdmin):
	list_display = ['name', 'review', 'rate']
admin.site.register(Review, ReviewAdmin)

class ReviewResponseAdmin(admin.ModelAdmin):
	list_display = ['user', 'response']
admin.site.register(ReviewResponse, ReviewResponseAdmin)




class SizeInline(admin.TabularInline):
	model = Size
	fk_name = 'size_set'


class SizeSetAdmin(admin.ModelAdmin):
	inlines = [SizeInline]
admin.site.register(SizeSet, SizeSetAdmin)


