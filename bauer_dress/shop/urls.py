from django.urls import path
from . import views
from promotion import views as promo_views
from orders import views as order_view


app_name = 'shop'
urlpatterns = [
    path('', promo_views.main, name='main'),
    path('shop/', views.product_list, name='index'),
    path('shop/for-rent/', views.for_rent, name='rent'),
    #path('new/', views.new_products, name='new'),
    #path('cheap-to-expensive/', views.cheap_product_list, name='sorting_cheap'),
    #path('expensive-to-cheap/', views.expensive_product_list, name='sorting_expensive'),
    path('rate/<int:id>/', views.rate_product, name='rate'),
    path('categories/<category_slug>/', views.product_list, name='index_by_category'),
    path('notification/<order_id>/<notification_id>/', views.admin_order_detail, name='notified_obj'),
    #path('material/<material_slug>/', views.product_list, name='index_by_model'),
    #path('models/<model_slug>/', views.product_list, name='index_by_material'),
    path('tags/<tag_slug>/', views.product_list, name='index_by_tag'),
    path('<category_slug>/<int:id>/<slug>/', views.product_detail, name='details'),
    path('<category_slug>/<int:id>/<slug>/<set_slug>/', views.product_set__detail, name='product_set__detail'),
    path('<int:review_id>/', views.review_response, name='response'),
]
