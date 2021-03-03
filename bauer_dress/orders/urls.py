from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    
    path('thank-you/<int:order_id>/', views.thank_you, name='thank_you'),
    path('finish/', views.finish, name='finish'),
    path('bad-results/', views.bad_results, name='bad_results'),
    path('order/<int:order_id>/', views.admin_order_detail,
    							name='admin_order_detail'),
    path('order/<int:order_id>/pdf/', views.admin_order_pdf,
    							name='admin_order_pdf'),
]