from django.contrib import admin
from .models import ShoppingCart, Item

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    inlines = [ItemInline]

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'reservation_id', 'shopping_cart')
