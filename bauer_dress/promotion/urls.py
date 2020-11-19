from django.urls import path
from . import views


app_name = 'promo'
urlpatterns = [
    path('shop/<slug>/', views.promo_products, name='index'),
    path('sub/', views.sub, name='sub')
]
