from django.urls import path 
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), 
        name='account_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='account_logout'),
    path('register/', views.UserCreateView.as_view(), name='account_signup'),
]