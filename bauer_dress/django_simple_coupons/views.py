from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import CouponApplyForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from django_simple_coupons.validations import validate_coupon
from django_simple_coupons.models import Coupon

from django.http import HttpResponse




@require_POST
def coupon_apply(request):
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        status = validate_coupon(coupon_code=code, user=request.user)
        if status['valid']:
            coupon = Coupon.objects.get(code=code)
            coupon.use_coupon(user=request.user)
            request.session['coupon_id'] = coupon.code
            messages.success(request, message='Купон активирован!')
            return redirect('cart:cart_detail')
        messages.error(request, message=status['message'])
        return redirect('cart:cart_detail')
    return redirect('cart:cart_detail')