from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import UserCreateForm
from django.contrib.messages.views import SuccessMessageMixin


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = "users/register.html"
    form_class = UserCreateForm
    success_url = '/login'
    success_message = 'Аккаунт для %(username)s был создан!'
