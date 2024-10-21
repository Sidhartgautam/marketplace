from django.db import models
from users.models import User
import uuid
from country.models import Country, Currency

# Create your models here.
class Store(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    currency =models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    seller = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    logo = models.ImageField(upload_to='store/logo', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    def __str__(self):
        return self.store_name
