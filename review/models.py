from django.db import models
from product.models import Product
from users.models import User
from core.utils.models import UUIDModel, TimeStampedModel

# Create your models here.
class ProductReview(UUIDModel, TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  # Ratings between 1-5
    review_text = models.TextField()
