from django.db import models
from order.models import Order

# Create your models here.
class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    tracking_number = models.CharField(max_length=255, unique=True)
    courier_company = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Lost', 'Lost'),
    ], default='In Transit')
    shipped_at = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)