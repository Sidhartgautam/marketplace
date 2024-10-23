# coupons/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from product.models import Product, Category
from users.models import User
from datetime import timezone
from core.utils.models import UUIDModel, TimeStampedModel

class Coupon(UUIDModel, TimeStampedModel):
    COUPON_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('free_shipping', 'Free Shipping'),
    ]
    code = models.CharField(max_length=20, unique=True, help_text="Unique code for the coupon.")
    type = models.CharField(max_length=20, choices=COUPON_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
        help_text="The discount value (percentage or fixed amount)."
    )
    min_purchase_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
        blank=True, null=True,
        help_text="Minimum purchase amount to use this coupon."
    )
    max_discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
        blank=True, null=True,
        help_text="Maximum discount this coupon can provide."
    )
    usage_limit = models.PositiveIntegerField(
        default=1,
        help_text="Number of times this coupon can be used."
    )
    used_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this coupon has been used."
    )
    start_date = models.DateTimeField(default=models.DateTimeField.now)
    expiration_date = models.DateTimeField(help_text="The date when the coupon expires.")
    active = models.BooleanField(default=True, help_text="Indicates if the coupon is currently active.")

    # Optional restrictions
    applicable_products = models.ManyToManyField(Product, blank=True, related_name='coupons')
    applicable_categories = models.ManyToManyField(Category, blank=True, related_name='coupons')
    applicable_users = models.ManyToManyField(User, blank=True, related_name='coupons')

    def __str__(self):
        return f"{self.code} ({self.type})"

    def is_valid(self, user=None, cart_total=None):
        """
        Check if the coupon is valid based on the provided conditions.
        """
        if not self.active:
            return False, "Coupon is not active."
        if self.expiration_date < timezone.now():
            return False, "Coupon has expired."
        if self.used_count >= self.usage_limit:
            return False, "Coupon usage limit has been reached."
        if self.min_purchase_amount and cart_total and cart_total < self.min_purchase_amount:
            return False, f"Minimum purchase amount of {self.min_purchase_amount} required."
        if user and self.applicable_users.exists() and user not in self.applicable_users.all():
            return False, "You are not eligible for this coupon."
        return True, "Coupon is valid."

    def calculate_discount(self, cart_total):
        """
        Calculate the discount amount based on the coupon type.
        """
        if self.type == 'percentage':
            discount = (self.discount_value / 100) * cart_total
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return round(discount, 2)
        elif self.type == 'fixed':
            return min(self.discount_value, cart_total)  # The discount can't exceed the cart total.
        elif self.type == 'free_shipping':
            return 0  # Typically handled separately in the shipping calculation.
        return 0

    def apply_coupon(self, user, cart_total):
        """
        Apply the coupon to the user's cart and calculate the final price.
        """
        is_valid, message = self.is_valid(user=user, cart_total=cart_total)
        if not is_valid:
            return cart_total, 0, message

        discount = self.calculate_discount(cart_total)
        self.used_count += 1
        self.save(update_fields=['used_count'])

        final_price = cart_total - discount
        return final_price, discount, "Coupon applied successfully."
