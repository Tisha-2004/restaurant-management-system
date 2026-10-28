from django.contrib import admin

from .models import Bill, BillItem


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "customer", "payment_method", "payment_status", "created_at")
    list_filter = ("payment_status", "payment_method")
    search_fields = ("invoice_number", "customer__name")
    inlines = [BillItemInline]
