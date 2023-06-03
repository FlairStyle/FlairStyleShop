from .models import Cart
from .models import CartItem
from django.contrib import admin


class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "date_added")
    readonly_fields = ("cart_id",)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product", "cart", "quantity", "is_active")


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
