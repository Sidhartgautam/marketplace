# coupons/serializers.py
from rest_framework import serializers
from coupons.models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'type', 'discount_value', 'min_purchase_amount',
            'max_discount_amount', 'usage_limit', 'used_count', 'start_date',
            'expiration_date', 'active', 'applicable_products', 'applicable_categories',
            'applicable_users'
        ]
        read_only_fields = ['used_count']
