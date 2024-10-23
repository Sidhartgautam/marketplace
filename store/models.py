from django.db import models
from users.models import User
import uuid
from country.models import Country, Currency
from core.utils.models import UUIDModel, TimeStampedModel

# Create your models here.
class Store(UUIDModel, TimeStampedModel):
    store_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    currency =models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store')
    logo = models.ImageField(upload_to='store/logo', blank=True, null=True)
    banner_image = models.ImageField(upload_to='store/banner', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    website_link = models.CharField(max_length=255, null=True, blank=True)
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    terms_and_conditions = models.TextField(blank=True, null=True)
    return_policy = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.store_name
    
    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        ordering = ['-created']
