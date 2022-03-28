from django.contrib import admin

from cart.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "status",
    ]
