from django.urls import path
from . import views


app_name = 'promo'
urlpatterns = [
    path('shop/<slug>/', views.promo_products, name='index'),
    path('shop/cheap-to-expensive/<slug>/', views.promo_sort_to_cheap, name='cheap'),
    path('shop/expensive-to-cheap/<slug>/', views.promo_sort_to_expensive, name='expensive'),
    path('sub/', views.sub, name='sub')
]
