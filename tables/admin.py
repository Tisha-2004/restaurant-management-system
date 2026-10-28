from django.contrib import admin

from .models import RestaurantTable


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ("number", "capacity", "status")
    list_filter = ("status",)
