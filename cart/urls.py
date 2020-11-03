from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
	path('', views.cart_detail, name='cart_detail'),
	path('clear/', views.cart_clear, name='cart_clear'),
	path('clear_coupon/', views.cart_clear_coupon, name='clear_coupon'),
	path('add/<product_id>/<price>/<product_set_slug>/', views.cart_add, name='cart_add'),
	path('remove/<product_id>/<price>/<color>/<quantity>/<product_set_slug>/', views.cart_remove, name='cart_remove')
]