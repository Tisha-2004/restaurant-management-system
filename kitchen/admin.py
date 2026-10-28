from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "table", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("number", "customer__name")
    inlines = [OrderItemInline]
