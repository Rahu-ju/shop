import csv
import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.urls import reverse

from .models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']



def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''
order_payment.short_description = 'stripe payment'



def export_to_csv(modeladmin, request, queryset):
    '''
    Docstring for export_to_csv
    It will create a CSV file from the current model, and selected objects from administrations site.
    modeladmin: current model
    request: current request
    QuerySet: current queryset
    '''

    #Get model options and generate csv file name and response object
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename="{opts.verbose_name}.csv"'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition

    # Write to the response object using csv writer object by feeding response object to it.
    writer = csv.writer(response)

    #Getting the model fields, excluding many to many and one to many.
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]

    # Now Write the header row
    writer.writerow([field.name for field in fields ])

    # Getting the data from the QuerySet and write the data row
    for obj in queryset:

        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)

        writer.writerow([data_row])

    return response

export_to_csv.short_description = 'Export to CSV'
    


def order_detail(obj):
    url = reverse("orders:admin_order_detail", args=[obj.id])
    return mark_safe(f'<a href="{url}">view</a>')



def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">pdf<a/>')



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'paid',
        order_payment,
        'created',
        'updated',
        order_detail,
        order_pdf
    ]

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
