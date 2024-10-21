from django.db import models

RESERVATION_IN_PROGRESS = '<reservation-in-progress>'

class ShoppingCart(models.Model):
    # The session ID will be the primary key for the ShoppingCart
    id = models.CharField(max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'ShoppingCart {self.id}'

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    reservation_id = models.CharField(max_length=100, default=RESERVATION_IN_PROGRESS)

    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items', null=True)

    def __str__(self):
        if self.shopping_cart:
            return f'Item {self.name} in Cart {self.shopping_cart.id}'
        return f'Items {self.name} without a Cart'