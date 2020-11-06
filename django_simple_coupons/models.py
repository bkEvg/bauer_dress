from django.db import models
from django.utils import timezone
from decimal import Decimal

from django_simple_coupons.helpers import (get_random_code,
                                           get_coupon_code_length,
                                           get_user_model)



class Ruleset(models.Model):
    allowed_users = models.ForeignKey('AllowedUsersRule', on_delete=models.CASCADE, verbose_name="Правило разрешений")
    max_uses = models.ForeignKey('MaxUsesRule', on_delete=models.CASCADE, verbose_name="Правило использований")
    validity = models.ForeignKey('ValidityRule', on_delete=models.CASCADE, verbose_name="Правило валидации")

    def __str__(self):
        return "Сет правил Nº{0}".format(self.id)

    class Meta:
        verbose_name = "сет правил"
        verbose_name_plural = "сеты правил"


class AllowedUsersRule(models.Model):
    user_model = get_user_model()

    users = models.ManyToManyField(user_model, verbose_name="Пользователи", blank=True)
    all_users = models.BooleanField(default=False, verbose_name="Все пользователи?")

    def __str__(self):
        return "Правило разрешений Nº{0}".format(self.id)

    class Meta:
        verbose_name = "правило разрешений"
        verbose_name_plural = "правила разрешений"


class MaxUsesRule(models.Model):
    max_uses = models.BigIntegerField(default=0, verbose_name="Макс. кол-во использований")
    is_infinite = models.BooleanField(default=False, verbose_name="Бесконечные использования?")
    uses_per_user = models.IntegerField(default=1, verbose_name="Использований для одного юзера")

    def __str__(self):
        return "Правило использований Nº{0}".   format(self.id)

    class Meta:
        verbose_name = "правило использований"
        verbose_name_plural = "правила использований"


class ValidityRule(models.Model):
    expiration_date = models.DateTimeField(verbose_name="Дата истечения")
    is_active = models.BooleanField(default=False, verbose_name="Активен?")

    def __str__(self):
        return "Правило валидации Nº{0}".   format(self.id)

    class Meta:
        verbose_name = "правило валидации"
        verbose_name_plural = "правила валидации"


class CouponUser(models.Model):
    user_model = get_user_model()

    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name="Пользователь")
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE, verbose_name="Купон")
    times_used = models.IntegerField(default=0, editable=False, verbose_name="Кол-во использованых раз")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "пользователь купона"
        verbose_name_plural = "пользователи купонов"


class Discount(models.Model):
    value = models.IntegerField(default=0, verbose_name="Значение")
    is_percentage = models.BooleanField(default=False, verbose_name="В процентах?")

    def __str__(self):
        if self.is_percentage:
            return "{0}% - Скидка".format(self.value)

        return "${0} - Скидка".format(self.value)

    class Meta:
        verbose_name = "скидка"
        verbose_name_plural = "скидки"


class Coupon(models.Model):
    code_length = get_coupon_code_length()

    code = models.CharField(max_length=code_length, default=get_random_code, verbose_name="Код купона", unique=True)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE, verbose_name="Скидка")
    times_used = models.IntegerField(default=0, editable=False, verbose_name="Использовано (раз)")
    created = models.DateTimeField(editable=False, verbose_name="Создан")

    ruleset = models.ForeignKey('Ruleset', on_delete=models.CASCADE, verbose_name="Сет правил")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "купон"
        verbose_name_plural = "купоны"

    def use_coupon(self, user):
        coupon_user, created = CouponUser.objects.get_or_create(user=user, coupon=self)
        coupon_user.times_used += 1
        coupon_user.save()

        self.times_used += 1
        self.save()

    def get_discount(self):
        return {
            "value": self.discount.value,
            "is_percentage": self.discount.is_percentage
        }
    
    def get_discounted_value(self, initial_value, extra=Decimal(0)):
        discount = self.get_discount()

        if discount['is_percentage']:
            new_price = initial_value - ((initial_value * discount['value']) / 100)
            new_price = new_price if new_price >= 0.0 else 0.0
        else:
            new_price = initial_value - discount['value']
            new_price = new_price if new_price >= 0.0 else 0.0

        return Decimal(new_price) + extra

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Coupon, self).save(*args, **kwargs)
