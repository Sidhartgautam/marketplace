from django.db import models
from product.models import ProductVariantCombination
from users.models import User
from core.utils.models import UUIDModel, TimeStampedModel
from django.core.exceptions import ValidationError

# Cart Model
class Cart(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    class Meta:
        unique_together = ('user', 'is_active')

# CartItem Model
class CartItem(UUIDModel, TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariantCombination, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product_variant}"

    def get_total_price(self):
        return self.product_variant.get_final_price() * self.quantity

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        if self.quantity > self.product_variant.stock:
            raise ValidationError("Not enough stock available.")
