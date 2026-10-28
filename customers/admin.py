from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "email", "date_joined")
    search_fields = ("name", "mobile", "email")
