from django.db import models
from users.models import User
from product.models import Product
from core.utils.models import UUIDModel, TimeStampedModel

class Wishlist(UUIDModel, TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"Wishlist of {self.user.username}"

class WishlistItem(UUIDModel, TimeStampedModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s wishlist"

    class Meta:
        unique_together = ('wishlist', 'product')