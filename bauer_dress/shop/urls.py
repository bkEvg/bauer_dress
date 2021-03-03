from django.urls import path
from . import views
from promotion import views as promo_views


app_name = 'shop'
urlpatterns = [
    path('', promo_views.main, name='main'),
    path('dresses/', views.dresses, name='dresses'),
    path('shop/', views.product_list, name='index'),
    path('shop/for-rent/', views.for_rent, name='rent'),
    path('rate/<int:id>/', views.rate_product, name='rate'),
    path('categories/<category_slug>/', views.product_list, name='index_by_category'),
    path('notification/<notification_id>/<order_id>/', views.notification_handler, name='notified_obj'),
    path('tags/<tag_slug>/', views.product_list, name='index_by_tag'),
    path('<category_slug>/<int:id>/<slug>/', views.product_detail, name='details'),
    path('<category_slug>/<int:id>/<slug>/<set_slug>/', views.product_set__detail, name='product_set__detail'),
    path('<int:review_id>/', views.review_response, name='response'),
]
