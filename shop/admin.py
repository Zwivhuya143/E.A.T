from django.contrib import admin
from shop.models import Product, SKU, Cart, CartItem, Order, OrderItem, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price", "image")    
    list_filter = ("name", "description",)    
    search_fields = ["name", "description"]

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title")
    
admin.site.register(Category)


class CartAdmin(admin.ModelAdmin):
    list_display = ("cart_id", "user", "cart_status")

admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart_item_id", "cart", "product", "quantity")
    list_filter = ("cart", "product",)
admin.site.register(CartItem, CartItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "address", "order_status", "total_price")
    list_filter = ("user", "order_status",)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order_item_id", "order", "product", "quantity")
    list_filter = ("order", "product",) 

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
