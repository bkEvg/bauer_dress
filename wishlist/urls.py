from django.urls import path
from . import views


app_name = 'wishlist'
urlpatterns = [
	path('', views.index, name='index'),
	# path('clear/', views.wishlist_clear, name='wishlist_clear'),
	path('cart-add/<product_id>/<price>/<product_set_slug>/', views.cart_add, name='cart_add'),
	path('remove/<product_id>/<price>/<quantity>/<product_set_slug>/', views.wishlist_remove, name='wishlist_remove'),
	path('wishlist-add/<product_id>/<price>/<product_set_slug>/', views.wishlist_add, name='wishlist_add'),
]