from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
import csv
import datetime


def order_detail(obj):
    return format_html('<a href="{}">О заказе</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))
order_detail.short_description = 'Подробнее'

def order_pdf(obj):
    return format_html('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])))
order_pdf.short_description = 'Счет PDF'


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Экспорт в CSV'



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    aw_in_fields = ['product']




class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'paid', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    search_fields = ['first_name__contains', 'last_name__contains', 'email__contains']
admin.site.register(Order, OrderAdmin)


