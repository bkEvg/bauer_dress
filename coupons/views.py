from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Coupon
from .forms import CouponApplyForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from django_simple_coupons.validations import validate_coupon
from django_simple_coupons.models import Coupon
from allauth.account.decorators import verified_email_required

from django.http import HttpResponse


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except ObjectDoesNotExist:
            request.session['coupon_id'] = {}
            messages.warning(request, message='Купон не найден!')
    return redirect('cart:cart_detail')

